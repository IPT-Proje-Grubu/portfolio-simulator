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
from src.ui.i18n import lang_manager

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
            return lang_manager.tr("Portföyünüz henüz boş. İşlem sayfasından ilk varlığınızı alın.")
        if max_conc > 70:
            return lang_manager.tr(
                "{sym} portföyünüzün %{max_conc:.0f}'ini oluşturuyor. "
                "ETH veya AAPL gibi farklı bir varlık alarak riski %50'nin altına çekin."
            ).format(sym=sym, max_conc=max_conc)
        if n_assets == 1:
            return lang_manager.tr(
                "Tek varlık (%{max_conc:.0f} {sym}) riski yüksek. "
                "En az 2 farklı varlık daha eklemeyi hedefleyin."
            ).format(max_conc=max_conc, sym=sym)
        if pnl > 0 and perf["total_trades"] >= 3:
            return lang_manager.tr(
                "Portföyünüz {pnl:+,.0f} TL kârda. "
                "Kâr realizasyonu için en yüksek kazançlı pozisyonu değerlendirin."
            ).format(pnl=pnl)
        if pnl < -p["starting_balance"] * 0.05:
            return lang_manager.tr(
                "Portföy %{abs_pct:.1f} zararda. Çeşitlendirme ile kalan riski azaltın."
            ).format(abs_pct=abs(perf['profit_loss_pct']))
        
        action = context.get("user_action", "")
        if action:
            return lang_manager.tr("İşlem tamamlandı. Portföy durumu: {risk_level} risk, {n_assets} varlık.").format(
                risk_level=risk['risk_level'], n_assets=n_assets
            )
            
        return lang_manager.tr("Portföy: {n_assets} varlık | Risk: {risk_level} | K/Z: {pnl:+,.0f} TL.").format(
            n_assets=n_assets, risk_level=risk['risk_level'], pnl=pnl
        )

    def qa_answer(self, context: dict, question: str) -> str:
        q    = question.lower()
        perf = context["performance"]
        risk = context["risk"]
        p    = context["portfolio"]
        learn = context["learning"]

        if any(kw in q for kw in ["risk", "tehlike", "güvenli", "danger"]):
            sym = risk.get("max_concentration_asset", "")
            return lang_manager.tr(
                "Risk seviyeniz: {risk_level} "
                "(%{max_conc:.0f} {sym} konsantrasyonu). "
                "Hedef: hiçbir varlık %50'yi geçmesin."
            ).format(risk_level=risk['risk_level'], max_conc=risk['max_concentration_pct'], sym=sym)
            
        if any(kw in q for kw in ["kâr", "kar", "kazanç", "profit", "zarar", "loss"]):
            return lang_manager.tr(
                "Toplam K/Z: {pnl:+,.0f} TL ({pnl_pct:+.1f}%). "
                "Gerçekleşmiş: {realized:+,.0f} TL | "
                "Gerçekleşmemiş: {unrealized:+,.0f} TL."
            ).format(
                pnl=perf['profit_loss'], 
                pnl_pct=perf['profit_loss_pct'], 
                realized=perf['realized_pnl'], 
                unrealized=perf['unrealized_pnl']
            )
            
        if any(kw in q for kw in ["çeşitlend", "diversif", "varlık", "asset"]):
            return lang_manager.tr(
                "Portföyünüzde {asset_count} farklı varlık var. "
                "5+ farklı varlık için ideal dağılım; her biri %30 altında tutulmalı."
            ).format(asset_count=risk['asset_count'])
            
        if any(kw in q for kw in ["ne alayım", "öner", "al ", "buy", "öneri"]):
            sym = risk.get("max_concentration_asset", "")
            ek = lang_manager.tr("Kripto ağırlıklı portföyünüze hisse veya emtia ekleyin.") if sym in ('BTC','ETH') else lang_manager.tr("Mevcut portföy dağılımınıza göre kripto veya emtia değerlendirin.")
            return lang_manager.tr("En az yatırım yaptığınız sektörü araştırın. {ek}").format(ek=ek)
            
        if any(kw in q for kw in ["görev", "task", "öğren", "learn"]):
            task = learn.get("current_task", "")
            return lang_manager.tr(
                "Şu anki görev: '{task}'. Seviye: {lvl} | XP: {xp}."
            ).format(
                task=task or lang_manager.tr('tümü tamamlandı'), 
                lvl=learn.get('current_level',''), 
                xp=learn.get('xp',0)
            )
            
        return lang_manager.tr(
            "Portföy: TL {val:,.0f} | K/Z: {pnl:+,.0f} TL | "
            "Risk: {risk_level} | {asset_count} varlık."
        ).format(
            val=p['total_value'], 
            pnl=perf['profit_loss'], 
            risk_level=risk['risk_level'], 
            asset_count=risk['asset_count']
        )

    def learning_hint(self, context: dict, task: "Task") -> str:
        _hints: dict[str, str] = {
            "buy_first_asset":       lang_manager.tr("İşlem (⇄) sayfasına git ve piyasa listesinden bir satıra tıkla."),
            "buy_with_amount":       lang_manager.tr("'Maksimum' butonuyla nakit bakiyenin büyük bir kısmını kullan."),
            "view_portfolio_summary":lang_manager.tr("Sol menüden '◎ Özet' simgesine tıkla."),
            "view_trade_history":    lang_manager.tr("Sol menüden '≡ Geçmiş' simgesine tıkla."),
            "first_sell":            lang_manager.tr("İşlem sayfasında SATIŞ moduna geç, Pozisyonlar tablosundan 'Kapat' butonu."),
            "diversify_portfolio":   lang_manager.tr("3 farklı sektörden varlık al: kripto, hisse, emtia."),
            "risk_under_50":         lang_manager.tr("Özet sayfasında portföy dağılımını kontrol et."),
            "profitable_trade":      lang_manager.tr("Pozisyonlar tablosunda yeşil K/Z gösteren varlığı sat."),
            "run_scenario_analysis": lang_manager.tr("Analiz sayfasında tarih seç → '▶ Senaryo Simülasyonu' butonu."),
            "check_forecast":        lang_manager.tr("Senaryo çalıştırdıktan sonra Analiz sayfasındaki tahmin tablosunu incele."),
        }
        hint = _hints.get(task.id, task.hint.split("→")[0].strip()[:100])
        return lang_manager.tr("İpucu: {hint}").format(hint=hint)


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