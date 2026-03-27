"""LearningManager — central coordinator for all learning-mode logic.

Architecture
------------
* LearningManager owns Level objects, each of which owns Task objects.
* Mutable progress state (_xp, _completed_tasks, …) lives here, not in Level/Task.
* check_all() is the single entry point called after every user action.
* Callbacks fire synchronously; UI binds to them to trigger toast notifications.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from src.learning.level import Level
from src.learning.task import Task

if TYPE_CHECKING:
    from src.portfolio.portfolio import PortfolioState


# ── Extra state (tracked by MainWindow, not PortfolioState) ───────────────────

@dataclass
class LearningExtra:
    """Thin record of UI-level events that PortfolioState cannot observe."""

    user_buy_count:        int   = 0
    user_sell_count:       int   = 0
    profitable_sell_count: int   = 0
    max_single_buy_tl:     float = 0.0
    dashboard_visited:     bool  = False
    history_visited:       bool  = False
    analysis_run:          bool  = False
    forecast_viewed:       bool  = False
    report_saved:          bool  = False
    calc_used:             bool  = False

    def to_dict(self) -> dict:
        return {
            "user_buy_count":        self.user_buy_count,
            "user_sell_count":       self.user_sell_count,
            "profitable_sell_count": self.profitable_sell_count,
            "max_single_buy_tl":     self.max_single_buy_tl,
            "dashboard_visited":     self.dashboard_visited,
            "history_visited":       self.history_visited,
            "analysis_run":          self.analysis_run,
            "forecast_viewed":       self.forecast_viewed,
            "report_saved":          self.report_saved,
            "calc_used":             self.calc_used,
        }


# ── Achievement & Challenge (kept here for clean imports) ─────────────────────

@dataclass
class Achievement:
    id: str
    title: str
    desc: str
    icon: str
    xp: int
    _validator: Callable[[Any, dict], bool]
    unlocked: bool = False

    def check(self, state: Any, extra: dict) -> bool:
        try:
            return bool(self._validator(state, extra))
        except Exception:
            return False


@dataclass
class Challenge:
    id: str
    title: str
    desc: str
    requirement: str
    icon: str
    xp: int
    _validator: Callable[[Any, dict], bool]
    completed: bool = False

    def check(self, state: Any, extra: dict) -> bool:
        try:
            return bool(self._validator(state, extra))
        except Exception:
            return False


# ── Validator helpers ──────────────────────────────────────────────────────────

def _v_risk_under_50(state: Any, _extra: dict) -> bool:
    pv = state.portfolio_value
    if pv <= 0 or not state.positions:
        return False
    return all(p.market_value / pv < 0.50 for p in state.positions)


def _v_balance_risk_reward(state: Any, _extra: dict) -> bool:
    if len(state.positions) < 5:
        return False
    pv = state.portfolio_value
    if pv <= 0:
        return False
    return all(p.market_value / pv < 0.30 for p in state.positions)


def _v_full_cycle(state: Any, extra: dict) -> bool:
    return (
        extra.get("user_buy_count", 0) >= 1
        and extra.get("user_sell_count", 0) >= 1
        and extra.get("analysis_run", False)
        and extra.get("report_saved", False)
    )


# ── LearningManager ───────────────────────────────────────────────────────────

class LearningManager:
    """
    Central learning system.

    Owns Level objects → Task lists.
    Tracks XP, completed tasks, unlocked achievements, completed challenges.
    Exposes backwards-compatible interface so existing code (learn_page.py,
    main_window.py) does not need to be rewritten after this refactor.
    """

    # Level metadata used by the UI
    LEVEL_ORDER: list[str] = ["beginner", "intermediate", "advanced"]

    LEVEL_META: dict[str, tuple[str, str]] = {
        "beginner":     ("🌱", "Başlangıç"),
        "intermediate": ("📈", "Orta"),
        "advanced":     ("🚀", "İleri"),
    }

    XP_THRESHOLDS: dict[str, int] = {
        "beginner":     0,
        "intermediate": 300,
        "advanced":     700,
        "master":       1200,
    }

    def __init__(self) -> None:
        self._xp:                   int       = 0
        self._completed_tasks:      set[str]  = set()
        self._unlocked_achievements: set[str] = set()
        self._completed_challenges: set[str]  = set()

        # Build structured objects
        self.levels:       list[Level]       = self._build_levels()
        self.achievements: list[Achievement] = self._build_achievements()
        self.challenges:   list[Challenge]   = self._build_challenges()

        # Flat task list for backwards-compat helpers
        self.tasks: list[Task] = [t for lvl in self.levels for t in lvl.tasks]

        # Event callbacks
        self._task_complete_cbs:   list[Callable[[Task, int], None]]    = []
        self._achievement_cbs:     list[Callable[[Achievement], None]]  = []
        self._level_up_cbs:        list[Callable[[str], None]]          = []
        self._level_complete_cbs:  list[Callable[[Level], None]]        = []

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def xp(self) -> int:
        return self._xp

    @property
    def current_level(self) -> str:
        level = "beginner"
        for lvl_id in self.LEVEL_ORDER:
            if self._xp >= self.XP_THRESHOLDS[lvl_id]:
                level = lvl_id
        return level

    @property
    def current_level_label(self) -> str:
        return self.LEVEL_META[self.current_level][1]

    @property
    def current_level_icon(self) -> str:
        return self.LEVEL_META[self.current_level][0]

    def level_progress(self) -> tuple[int, int]:
        """Returns (xp_earned_in_level, xp_needed_to_complete_level)."""
        lvl   = self.current_level
        start = self.XP_THRESHOLDS[lvl]
        idx   = self.LEVEL_ORDER.index(lvl)
        end   = (
            self.XP_THRESHOLDS[self.LEVEL_ORDER[idx + 1]]
            if idx + 1 < len(self.LEVEL_ORDER)
            else self.XP_THRESHOLDS.get("master", 1200)
        )
        return self._xp - start, max(end - start, 1)

    # ── Level queries ─────────────────────────────────────────────────────────

    def get_level(self, level_id: str) -> Level | None:
        return next((l for l in self.levels if l.id == level_id), None)

    def is_level_unlocked(self, level_id: str) -> bool:
        return self._xp >= self.XP_THRESHOLDS.get(level_id, 0)

    # ── Task queries (backwards-compat interface used by learn_page.py) ───────

    def tasks_for_level(self, level_id: str) -> list[Task]:
        lvl = self.get_level(level_id)
        return lvl.tasks if lvl else []

    def is_task_locked(self, task: Task) -> bool:
        lvl = self.get_level(task.level_id)
        if not lvl:
            return True
        return lvl.is_task_locked(task, self._completed_tasks, self._xp)

    def is_task_complete(self, task_id: str) -> bool:
        return task_id in self._completed_tasks

    def completed_count(self, level_id: str) -> int:
        lvl = self.get_level(level_id)
        return lvl.completed_count(self._completed_tasks) if lvl else 0

    def total_tasks(self, level_id: str) -> int:
        lvl = self.get_level(level_id)
        return lvl.total_task_count() if lvl else 0

    # ── Main update entry point ────────────────────────────────────────────────

    def check_all(self, state: Any, extra: dict) -> list[str]:
        """
        Validate all unlocked tasks and achievements.
        Returns list of newly completed task IDs.
        Fires registered callbacks for each completion event.
        """
        newly_completed: list[str] = []
        prev_level = self.current_level

        for task in self.tasks:
            if task.id in self._completed_tasks:
                continue
            if self.is_task_locked(task):
                continue
            if task.validate(state, extra):
                self._completed_tasks.add(task.id)
                self._xp += task.xp
                newly_completed.append(task.id)
                for cb in self._task_complete_cbs:
                    cb(task, task.xp)
                # Check if level just became complete
                lvl = self.get_level(task.level_id)
                if lvl and lvl.is_complete(self._completed_tasks):
                    for cb in self._level_complete_cbs:
                        cb(lvl)

        for ach in self.achievements:
            if ach.id in self._unlocked_achievements:
                continue
            if ach.check(state, extra):
                ach.unlocked = True
                self._unlocked_achievements.add(ach.id)
                self._xp += ach.xp
                for cb in self._achievement_cbs:
                    cb(ach)

        for ch in self.challenges:
            if ch.id in self._completed_challenges:
                continue
            if ch.check(state, extra):
                ch.completed = True
                self._completed_challenges.add(ch.id)
                self._xp += ch.xp

        new_level = self.current_level
        if new_level != prev_level:
            for cb in self._level_up_cbs:
                cb(new_level)

        return newly_completed

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def on_task_complete(self, cb: Callable[[Task, int], None]) -> None:
        self._task_complete_cbs.append(cb)

    def on_achievement_unlock(self, cb: Callable[[Achievement], None]) -> None:
        self._achievement_cbs.append(cb)

    def on_level_up(self, cb: Callable[[str], None]) -> None:
        self._level_up_cbs.append(cb)

    def on_level_complete(self, cb: Callable[[Level], None]) -> None:
        self._level_complete_cbs.append(cb)

    # ── Analytics ─────────────────────────────────────────────────────────────

    @staticmethod
    def get_analytics(state: Any) -> dict:
        if not state.trade_history:
            return {}
        buys  = [t for t in state.trade_history if t.side == "AL"]
        sells = [t for t in state.trade_history if t.side == "SAT"]
        best  = max(sells, key=lambda t: t.total, default=None)
        worst = min(sells, key=lambda t: t.total, default=None)
        pv    = state.portfolio_value
        risk  = "Bilinmiyor"
        if pv > 0 and state.positions:
            w    = max(p.market_value / pv for p in state.positions) * 100
            risk = "Düşük" if w < 30 else ("Orta" if w < 60 else "Yüksek")
        return {
            "total_trades":    len(state.trade_history),
            "buy_count":       len(buys),
            "sell_count":      len(sells),
            "total_volume":    sum(t.total for t in state.trade_history),
            "total_pnl":       state.total_pnl,
            "realized_pnl":    state.total_realized_pnl,
            "unrealized_pnl":  state.total_unrealized_pnl,
            "best_trade":      best,
            "worst_trade":     worst,
            "risk_level":      risk,
            "portfolio_value": pv,
        }

    def get_level_summary(self, level_id: str, state: Any) -> dict:
        """Return performance summary for a completed level."""
        lvl = self.get_level(level_id)
        if not lvl:
            return {}
        analytics  = self.get_analytics(state)
        tasks_done = lvl.completed_count(self._completed_tasks)
        earned_xp  = lvl.earned_xp(self._completed_tasks)
        return {
            "level_name":  lvl.name,
            "level_icon":  lvl.icon,
            "tasks_done":  tasks_done,
            "total_tasks": lvl.total_task_count(),
            "earned_xp":   earned_xp,
            **analytics,
        }

    # ── Data builders ──────────────────────────────────────────────────────────

    @staticmethod
    def _build_levels() -> list[Level]:
        return [
            Level(
                id="beginner",
                name="Başlangıç",
                icon="🌱",
                xp_required=0,
                tasks=[
                    Task(
                        id="buy_first_asset",
                        title="İlk Varlık Alımı",
                        description="Herhangi bir varlığı satın al.",
                        objective="İşlem sayfasında herhangi bir varlıktan en az 1 adet satın al.",
                        hint="'İşlem (⇄)' sayfasına git → piyasa listesinden bir satıra tıkla → miktar gir → İŞLEM GERÇEKLEŞTIR butonuna bas.",
                        xp=100, icon="🛒", level_id="beginner", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("user_buy_count", 0) >= 1,
                    ),
                    Task(
                        id="buy_with_amount",
                        title="Büyük Yatırım",
                        description="Tek işlemde TL 10.000+ değerinde varlık al.",
                        objective="Toplam değeri TL 10.000 veya daha fazla olan tek bir alım işlemi gerçekleştir.",
                        hint="'Maksimum' butonuna basarak mevcut nakdin tamamını veya büyük bir kısmını tek işlemde kullan.",
                        xp=150, icon="💵", level_id="beginner", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("max_single_buy_tl", 0) >= 10_000,
                    ),
                    Task(
                        id="view_portfolio_summary",
                        title="Portföy İnceleme",
                        description="Özet sayfasına giderek portföy değerini ve K/Z'yı incele.",
                        objective="Sol menüden Özet (◎) sayfasına git ve 4 metrik kartını gözlemle.",
                        hint="Sol kenar çubuğundan '◎ Özet' simgesine tıkla. Portföy Değeri, K/Z ve Nakit rakamlarını incele.",
                        xp=50, icon="📊", level_id="beginner", navigate_to=0, navigate_label="→ Özet Sayfası",
                        _validator=lambda s, e: e.get("dashboard_visited", False),
                    ),
                    Task(
                        id="view_trade_history",
                        title="İşlem Geçmişi",
                        description="Geçmiş sayfasını ziyaret ederek tüm işlemleri görüntüle.",
                        objective="'Geçmiş (≡)' sayfasına git ve işlem tablosunu kontrol et.",
                        hint="Sol menüden '≡ Geçmiş' simgesine tıkla. Tüm alım/satım işlemlerini ve istatistikleri görebilirsin.",
                        xp=50, icon="📋", level_id="beginner", navigate_to=2, navigate_label="→ Geçmiş Sayfası",
                        _validator=lambda s, e: e.get("history_visited", False),
                    ),
                    Task(
                        id="first_sell",
                        title="İlk Satış",
                        description="Elindeki herhangi bir varlığı sat.",
                        objective="Mevcut pozisyonlarından birini tamamen veya kısmen sat.",
                        hint="'İşlem (⇄)' sayfasında 'SATIŞ' moduna geç → Pozisyonlar tablosundan 'Pozisyonu Kapat' butonunu kullan ya da sembolü elle gir.",
                        xp=150, icon="💰", level_id="beginner", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("user_sell_count", 0) >= 1,
                    ),
                ],
            ),
            Level(
                id="intermediate",
                name="Orta",
                icon="📈",
                xp_required=300,
                tasks=[
                    Task(
                        id="diversify_portfolio",
                        title="Portföy Çeşitlendirme",
                        description="En az 3 farklı varlığa aynı anda sahip ol.",
                        objective="Portföyünde eş zamanlı olarak en az 3 farklı varlık bulundur.",
                        hint="BTC, ETH, AAPL, NVDA, GOLD gibi farklı sektörlerden varlık al. Çeşitlendirme riski dağıtır.",
                        xp=150, icon="🌐", level_id="intermediate", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: len(s.positions) >= 3,
                    ),
                    Task(
                        id="risk_under_50",
                        title="Risk Dengesi",
                        description="Hiçbir varlık portföyün %50'sini geçmesin.",
                        objective="Portföydeki her varlığın ağırlığını en fazla %50 ile sınırla.",
                        hint="Özet sayfasındaki portföy dağılımını kontrol et. Tek bir varlığa aşırı yoğunlaşma riskini artırır.",
                        xp=150, icon="⚖️", level_id="intermediate", navigate_to=0, navigate_label="→ Portföy Kontrolü",
                        _validator=_v_risk_under_50,
                    ),
                    Task(
                        id="profitable_trade",
                        title="Karlı İşlem",
                        description="Bir varlığı alış fiyatından yüksek fiyata sat.",
                        objective="Alış maliyetinin üzerindeki bir fiyata satış yaparak gerçekleşmiş kâr elde et.",
                        hint="Fiyatlar her 3 saniyede değişiyor. Pozisyonlar tablosundaki yeşil K/Z değerleri kâr edilebilecek pozisyonları gösterir.",
                        xp=200, icon="📈", level_id="intermediate", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("profitable_sell_count", 0) >= 1,
                    ),
                    Task(
                        id="run_scenario_analysis",
                        title="Senaryo Analizi",
                        description="Analiz sekmesinde bir senaryo simülasyonu çalıştır.",
                        objective="Analiz sayfasında tarih aralığı seçip simülasyonu başlat ve sonuçları incele.",
                        hint="'Analiz (⊙)' sayfasına git → Başlangıç/bitiş tarihlerini seçimi yap → '▶ Senaryo Simülasyonu' butonuna bas.",
                        xp=200, icon="🔬", level_id="intermediate", navigate_to=4, navigate_label="→ Analiz Sayfası",
                        _validator=lambda s, e: e.get("analysis_run", False),
                    ),
                    Task(
                        id="check_forecast",
                        title="Tahmin Tablosunu İncele",
                        description="Senaryo sonuçlarını ve tahmin noktalarını görüntüle.",
                        objective="Analiz çalıştırdıktan sonra Analiz sayfasındaki Tahmin Noktaları tablosunu kontrol et.",
                        hint="Önce 'Senaryo Analizi' görevini bitir. Ardından Analiz sayfasına dön — sağdaki tahmin tablosunu incele.",
                        xp=100, icon="🔭", level_id="intermediate", navigate_to=4, navigate_label="→ Analiz Sayfası",
                        _validator=lambda s, e: e.get("analysis_run", False) and e.get("forecast_viewed", False),
                    ),
                ],
            ),
            Level(
                id="advanced",
                name="İleri",
                icon="🚀",
                xp_required=700,
                tasks=[
                    Task(
                        id="maximize_profit",
                        title="Kâr Maksimizasyonu",
                        description="2+ karlı satış ile pozitif gerçekleşmiş K/Z elde et.",
                        objective="En az 2 karlı satış gerçekleştirerek toplam gerçekleşmiş K/Z'nı sıfırın üzerine taşı.",
                        hint="Alış maliyetinin üzerindeki fiyatlarda sat. Her işlemin ardından 'Geçmiş' sayfasında K/Z'ı takip et.",
                        xp=250, icon="💰", level_id="advanced", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("profitable_sell_count", 0) >= 2 and s.total_realized_pnl > 0,
                    ),
                    Task(
                        id="survive_simulation",
                        title="Simülasyon Direnci",
                        description="Senaryo simülasyonu sonrası portföy değerini %80+ tut.",
                        objective="Simülasyonu çalıştır ve portföy değerin başlangıç bakiyesinin en az %80'i olsun.",
                        hint="Çeşitlendirilmiş portföy simülasyonlarda daha dirençlidir. 3+ farklı varlık tut, ağırlıkları dengeli dağıt.",
                        xp=200, icon="🛡️", level_id="advanced", navigate_to=4, navigate_label="→ Analiz Sayfası",
                        _validator=lambda s, e: e.get("analysis_run", False) and s.portfolio_value >= s.starting_balance * 0.80,
                    ),
                    Task(
                        id="balance_risk_reward",
                        title="Risk-Getiri Dengesi",
                        description="5+ farklı varlık tut, hiçbiri %30'u aşmasın.",
                        objective="En az 5 farklı varlığa sahip ol ve her birinin ağırlığı portföyün %30'unu geçmesin.",
                        hint="Kripto (BTC, ETH), hisse (AAPL, NVDA), emtia (GOLD, OIL) gibi farklı sınıflardan al. Denge risk-getiriyi optimize eder.",
                        xp=300, icon="🎯", level_id="advanced", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=_v_balance_risk_reward,
                    ),
                    Task(
                        id="profitable_sequence",
                        title="Karlı Seri",
                        description="3 veya daha fazla karlı satış gerçekleştir.",
                        objective="Birden fazla pozisyonu kâr ile kapatarak 3+ karlı satış sayısına ulaş.",
                        hint="Fiyatların yükseldiği dönemleri bekle. Pozisyonlar tablosundaki her yeşil K/Z satırı kâr fırsatını gösterir.",
                        xp=300, icon="🔥", level_id="advanced", navigate_to=1, navigate_label="→ İşlem Sayfası",
                        _validator=lambda s, e: e.get("profitable_sell_count", 0) >= 3,
                    ),
                    Task(
                        id="complete_full_cycle",
                        title="Tam Döngü",
                        description="Al → Analiz Et → Sat → Rapor Kaydet döngüsünü tamamla.",
                        objective="Bir alım yap, senaryo analizi çalıştır, satış gerçekleştir ve raporu dosyaya kaydet.",
                        hint="Sırayla: İşlem sayfasında alım → Analiz sayfasında simülasyon → İşlem sayfasında satış → Rapor Kaydet butonu.",
                        xp=400, icon="🔄", level_id="advanced", navigate_to=4, navigate_label="→ Analiz Sayfası",
                        _validator=_v_full_cycle,
                    ),
                ],
            ),
        ]

    @staticmethod
    def _build_achievements() -> list[Achievement]:
        return [
            Achievement(id="first_trade",    title="İlk İşlem",       desc="İlk alım işlemini gerçekleştir.",               icon="🎯", xp=50,  _validator=lambda s, e: e.get("user_buy_count", 0) >= 1),
            Achievement(id="risk_manager",   title="Risk Yöneticisi", desc="2+ varlıkla portföy riskini dengede tut.",      icon="🛡️", xp=100, _validator=lambda s, e: _v_risk_under_50(s, e) and len(s.positions) >= 2),
            Achievement(id="diversifier",    title="Çeşitlendirici",  desc="5 farklı varlığa aynı anda sahip ol.",          icon="🌐", xp=150, _validator=lambda s, e: len(s.positions) >= 5),
            Achievement(id="profitable",     title="Karlı Çıkış",     desc="Bir varlığı karlı şekilde sat.",                icon="💎", xp=150, _validator=lambda s, e: e.get("profitable_sell_count", 0) >= 1),
            Achievement(id="analyst",        title="Analist",         desc="Senaryo analizini çalıştır.",                   icon="🔬", xp=100, _validator=lambda s, e: e.get("analysis_run", False)),
            Achievement(id="veteran",        title="Veteran",         desc="Toplam 10+ işlem gerçekleştir.",                icon="🏅", xp=200, _validator=lambda s, e: len(s.trade_history) >= 10),
            Achievement(id="big_portfolio",  title="Büyük Portföy",   desc="Portföy değerini başlangıçtan %10 artır.",      icon="💰", xp=200, _validator=lambda s, e: s.portfolio_value > s.starting_balance * 1.10),
            Achievement(id="careful_trader", title="Temkinli Trader", desc="20+ işlem yap, realized P/L pozitif kalsın.",   icon="🧠", xp=250, _validator=lambda s, e: len(s.trade_history) >= 20 and s.total_realized_pnl > 0),
        ]

    @staticmethod
    def _build_challenges() -> list[Challenge]:
        return [
            Challenge(
                id="triple_profit",
                title="Üçlü Kârcı",
                desc="Borsada 3 farklı satış işleminde kâr elde et.",
                requirement="3 karlı satış gerçekleştir",
                icon="🔥", xp=300,
                _validator=lambda s, e: e.get("profitable_sell_count", 0) >= 3,
            ),
            Challenge(
                id="diversification_master",
                title="Çeşitlendirme Ustası",
                desc="Hiçbir varlığın ağırlığı %30'u geçmeden en az 4 varlık tut.",
                requirement="4+ varlık, her biri en fazla %30 ağırlık",
                icon="⚡", xp=250,
                _validator=lambda s, e: (
                    len(s.positions) >= 4 and s.portfolio_value > 0 and
                    max((p.market_value / s.portfolio_value for p in s.positions), default=1) < 0.30
                ),
            ),
            Challenge(
                id="full_analyst",
                title="Tam Analist",
                desc="Analiz çalıştır, tahmini incele ve raporu kaydet.",
                requirement="Senaryo analizi + tahmin görüntüleme + rapor kaydetme",
                icon="📊", xp=200,
                _validator=lambda s, e: (
                    e.get("analysis_run", False) and
                    e.get("forecast_viewed", False) and
                    e.get("report_saved", False)
                ),
            ),
        ]
