"""AICoach — Hybrid AI system: rule-based primary + Gemini enhancement layer.

Flow for every coaching request:
  1. ContextBuilder assembles structured context from live state.
  2. Rule-based engine produces a concrete fallback message.
  3. If Gemini is available, a GeminiWorker sends the context asynchronously.
  4. UI callback receives either the AI response or the rule-based fallback.

This design guarantees the app is always usable even when offline.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from src.ai.context_builder import ContextBuilder
from src.ai.gemini_service import GeminiService, GeminiWorker

if TYPE_CHECKING:
    from src.learning.manager import LearningManager
    from src.learning.task import Task
    from src.portfolio.portfolio import PortfolioState


# ── Rule-based fallback engine ────────────────────────────────────────────────

class _RuleEngine:
    """
    Produces deterministic, data-driven coaching messages without API calls.
    Always runs first; Gemini refines the output if available.
    """

    def action_suggestion(self, context: dict) -> str:
        p    = context["portfolio"]
        perf = context["performance"]
        risk = context["risk"]

        warnings = risk.get("warnings", [])
        if warnings:
            return warnings[0]

        max_conc = risk["max_concentration_pct"]
        sym      = risk.get("max_concentration_asset", "")
        n_assets = risk["asset_count"]
        pnl      = perf["profit_loss"]

        if n_assets == 0:
            return "Portföyünüz henüz boş. İşlem sayfasından ilk varlığınızı alın."
        if max_conc > 70:
            return (
                f"{sym} portföyünüzün %{max_conc:.0f}'ini oluşturuyor. "
                f"ETH veya AAPL gibi farklı bir varlık alarak riski %50'nin altına çekin."
            )
        if n_assets == 1:
            return (
                f"Tek varlık (%{max_conc:.0f} {sym}) riski yüksek. "
                f"En az 2 farklı varlık daha eklemeyi hedefleyin."
            )
        if pnl > 0 and perf["total_trades"] >= 3:
            return (
                f"Portföyünüz {pnl:+,.0f} TL kârda. "
                f"Kâr realizasyonu için en yüksek kazançlı pozisyonu değerlendirin."
            )
        if pnl < -p["starting_balance"] * 0.05:
            return (
                f"Portföy %{abs(perf['profit_loss_pct']):.1f} zararda. "
                f"Çeşitlendirme ile kalan riski azaltın."
            )
        action = context.get("user_action", "")
        if action:
            return f"İşlem tamamlandı. Portföy durumu: {risk['risk_level']} risk, {n_assets} varlık."
        return f"Portföy: {n_assets} varlık | Risk: {risk['risk_level']} | K/Z: {pnl:+,.0f} TL."

    def qa_answer(self, context: dict, question: str) -> str:
        q    = question.lower()
        perf = context["performance"]
        risk = context["risk"]
        p    = context["portfolio"]
        learn = context["learning"]

        if any(kw in q for kw in ["risk", "tehlike", "güvenli", "danger"]):
            sym = risk.get("max_concentration_asset", "")
            return (
                f"Risk seviyeniz: {risk['risk_level']} "
                f"(%{risk['max_concentration_pct']:.0f} {sym} konsantrasyonu). "
                f"Hedef: hiçbir varlık %50'yi geçmesin."
            )
        if any(kw in q for kw in ["kâr", "kar", "kazanç", "profit", "zarar", "loss"]):
            return (
                f"Toplam K/Z: {perf['profit_loss']:+,.0f} TL ({perf['profit_loss_pct']:+.1f}%). "
                f"Gerçekleşmiş: {perf['realized_pnl']:+,.0f} TL | "
                f"Gerçekleşmemiş: {perf['unrealized_pnl']:+,.0f} TL."
            )
        if any(kw in q for kw in ["çeşitlend", "diversif", "varlık", "asset"]):
            return (
                f"Portföyünüzde {risk['asset_count']} farklı varlık var. "
                f"5+ farklı varlık için ideal dağılım; her biri %30 altında tutulmalı."
            )
        if any(kw in q for kw in ["ne alayım", "öner", "al ", "buy", "öneri"]):
            sym = risk.get("max_concentration_asset", "")
            return (
                f"En az yatırım yaptığınız sektörü araştırın. "
                f"{'Kripto ağırlıklı portföyünüze hisse veya emtia ekleyin.' if sym in ('BTC','ETH') else 'Mevcut portföy dağılımınıza göre kripto veya emtia değerlendirin.'}"
            )
        if any(kw in q for kw in ["görev", "task", "öğren", "learn"]):
            task = learn.get("current_task", "")
            return (
                f"Şu anki görev: '{task or 'tümü tamamlandı'}'. "
                f"Seviye: {learn.get('current_level','')} | XP: {learn.get('xp',0)}."
            )
        return (
            f"Portföy: TL {p['total_value']:,.0f} | "
            f"K/Z: {perf['profit_loss']:+,.0f} TL | "
            f"Risk: {risk['risk_level']} | {risk['asset_count']} varlık."
        )

    def learning_hint(self, context: dict, task: "Task") -> str:
        _hints: dict[str, str] = {
            "buy_first_asset":       "İşlem (⇄) sayfasına git ve piyasa listesinden bir satıra tıkla.",
            "buy_with_amount":       "'Maksimum' butonuyla nakit bakiyenin büyük bir kısmını kullan.",
            "view_portfolio_summary":"Sol menüden '◎ Özet' simgesine tıkla.",
            "view_trade_history":    "Sol menüden '≡ Geçmiş' simgesine tıkla.",
            "first_sell":            "İşlem sayfasında SATIŞ moduna geç, Pozisyonlar tablosundan 'Kapat' butonu.",
            "diversify_portfolio":   "3 farklı sektörden varlık al: kripto, hisse, emtia.",
            "risk_under_50":         "Özet sayfasında portföy dağılımını kontrol et.",
            "profitable_trade":      "Pozisyonlar tablosunda yeşil K/Z gösteren varlığı sat.",
            "run_scenario_analysis": "Analiz sayfasında tarih seç → '▶ Senaryo Simülasyonu' butonu.",
            "check_forecast":        "Senaryo çalıştırdıktan sonra Analiz sayfasındaki tahmin tablosunu incele.",
        }
        hint = _hints.get(task.id, task.hint.split("→")[0].strip()[:100])
        return f"İpucu: {hint}"


# ── AICoach ───────────────────────────────────────────────────────────────────

class AICoach:
    """
    Hybrid AI Coach.

    Public API
    ----------
    get_action_suggestion(state, extra, ls, action, callback)
        → fires callback(message) asynchronously (or synchronously if no Gemini)

    answer_question(state, extra, ls, question, callback)
        → same pattern

    get_learning_hint(state, extra, ls, task, callback)
        → same pattern, but Gemini is prompted for a hint (not solution)

    build_context(state, extra, ls, action="")
        → returns the raw context dict (useful for diagnostics / display)
    """

    def __init__(
        self,
        gemini: GeminiService,
        ctx_builder: ContextBuilder,
    ) -> None:
        self._gemini      = gemini
        self._ctx_builder = ctx_builder
        self._rules       = _RuleEngine()
        self._workers: list[GeminiWorker] = []   # keep refs alive

    # ── Public helpers ────────────────────────────────────────────────────────

    @property
    def gemini_available(self) -> bool:
        return self._gemini.is_available

    @property
    def gemini_status(self) -> str:
        return self._gemini.status_message

    def build_context(
        self,
        state: "PortfolioState",
        extra: Any,
        ls: "LearningManager",
        action: str = "",
        lb: Any = None,
    ) -> dict:
        return self._ctx_builder.build(state, extra, ls, last_action=action, lb=lb)

    # ── Core coaching methods ─────────────────────────────────────────────────

    def get_action_suggestion(
        self,
        state: "PortfolioState",
        extra: Any,
        ls: "LearningManager",
        action: str,
        callback: Callable[[str], None],
        lb: Any = None,
    ) -> None:
        context  = self.build_context(state, extra, ls, action, lb)
        fallback = self._rules.action_suggestion(context)
        self._dispatch(context, None, fallback, callback)

    def answer_question(
        self,
        state: "PortfolioState",
        extra: Any,
        ls: "LearningManager",
        question: str,
        callback: Callable[[str], None],
        lb: Any = None,
    ) -> None:
        context  = self.build_context(state, extra, ls, lb=lb)
        fallback = self._rules.qa_answer(context, question)
        self._dispatch(context, question, fallback, callback)

    def get_learning_hint(
        self,
        state: "PortfolioState",
        extra: Any,
        ls: "LearningManager",
        task: "Task",
        callback: Callable[[str], None],
        lb: Any = None,
    ) -> None:
        context  = self.build_context(state, extra, ls, lb=lb)
        fallback = self._rules.learning_hint(context, task)
        question = (
            f"The user is on learning task '{task.title}': {task.objective}. "
            f"Give a 1-sentence hint only — do NOT give the full solution."
        )
        self._dispatch(context, question, fallback, callback)

    # ── Dispatch helper ───────────────────────────────────────────────────────

    def _dispatch(
        self,
        context: dict,
        question: str | None,
        fallback: str,
        callback: Callable[[str], None],
    ) -> None:
        if not self._gemini.is_available:
            callback(fallback)
            return

        worker = self._gemini.make_worker(context, question, fallback)
        worker.result_ready.connect(callback)
        worker.failed.connect(callback)
        worker.finished.connect(lambda: self._cleanup(worker))
        self._workers.append(worker)
        worker.start()

    def _cleanup(self, worker: GeminiWorker) -> None:
        try:
            self._workers.remove(worker)
        except ValueError:
            pass
