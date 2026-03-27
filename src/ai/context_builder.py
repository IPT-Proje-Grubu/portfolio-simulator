"""ContextBuilder — assembles a structured, AI-ready context from live app state.

The context dict is the single source of truth passed to both the rule-based
system and Gemini.  It is serialisable (no PyQt objects, no circular refs).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.learning.leaderboard import LeaderboardManager
    from src.learning.manager import LearningManager
    from src.learning.mistake_detector import MistakeDetector
    from src.portfolio.portfolio import PortfolioState


class ContextBuilder:
    """
    Builds a structured context dict from PortfolioState + learning state.

    Usage::

        builder = ContextBuilder(detector=mistake_detector)
        ctx = builder.build(state, extra, learning_manager, last_action="Bought BTC TL 15,000")
    """

    def __init__(self, detector: "MistakeDetector | None" = None) -> None:
        self._detector = detector

    def build(
        self,
        state: "PortfolioState",
        extra: Any,                     # LearningExtra or plain dict
        ls: "LearningManager",
        last_action: str = "",
        lb: "LeaderboardManager | None" = None,
    ) -> dict:
        extra_d: dict = extra.to_dict() if hasattr(extra, "to_dict") else dict(extra)

        portfolio   = self._build_portfolio(state)
        performance = self._build_performance(state, extra_d)
        risk        = self._build_risk(state, portfolio["assets"])
        learning    = self._build_learning(ls)
        leaderboard = self._build_leaderboard(lb, ls) if lb else {}

        return {
            "portfolio":   portfolio,
            "performance": performance,
            "risk":        risk,
            "learning":    learning,
            "leaderboard": leaderboard,
            "user_action": last_action,
        }

    # ── Section builders ──────────────────────────────────────────────────────

    def _build_portfolio(self, state: "PortfolioState") -> dict:
        pv = state.portfolio_value
        assets: list[dict] = []
        for pos in state.positions:
            weight = pos.market_value / pv * 100 if pv > 0 else 0.0
            assets.append({
                "symbol":        pos.symbol,
                "quantity":      pos.quantity,
                "avg_cost":      pos.avg_cost,
                "current_price": pos.current_price,
                "market_value":  pos.market_value,
                "pnl":           pos.unrealized_pnl,
                "pnl_pct":       pos.unrealized_pnl_pct * 100,
                "weight_pct":    round(weight, 2),
            })

        distribution = {a["symbol"]: round(a["weight_pct"], 1) for a in assets}
        distribution["CASH"] = round(state.cash / pv * 100, 1) if pv > 0 else 100.0

        return {
            "total_value":       round(pv, 2),
            "cash":              round(state.cash, 2),
            "starting_balance":  round(state.starting_balance, 2),
            "assets":            assets,
            "distribution":      distribution,
            "position_count":    len(assets),
        }

    def _build_performance(self, state: "PortfolioState", extra_d: dict) -> dict:
        sells = [t for t in state.trade_history if t.side == "SAT"]
        buys  = [t for t in state.trade_history if t.side == "AL"]
        best  = max(sells, key=lambda t: t.total, default=None)
        worst = min(sells, key=lambda t: t.total, default=None)

        win_rate = (
            round(extra_d.get("profitable_sell_count", 0) / len(sells) * 100, 1)
            if sells else 0.0
        )

        return {
            "profit_loss":       round(state.total_pnl, 2),
            "profit_loss_pct":   round(state.total_pnl_pct * 100, 2),
            "realized_pnl":      round(state.total_realized_pnl, 2),
            "unrealized_pnl":    round(state.total_unrealized_pnl, 2),
            "total_trades":      len(state.trade_history),
            "buy_count":         len(buys),
            "sell_count":        len(sells),
            "profitable_sells":  extra_d.get("profitable_sell_count", 0),
            "win_rate_pct":      win_rate,
            "best_trade":        f"{best.symbol} TL {best.total:,.0f}" if best else None,
            "worst_trade":       f"{worst.symbol} TL {worst.total:,.0f}" if worst else None,
            "total_volume":      round(sum(t.total for t in state.trade_history), 2),
        }

    def _build_risk(self, state: "PortfolioState", assets: list[dict]) -> dict:
        if not assets:
            return {
                "risk_score": 0.0, "risk_level": "Belirsiz",
                "max_concentration_pct": 0.0, "max_concentration_asset": None,
                "asset_count": 0, "warnings": [],
            }

        weights = [(a["symbol"], a["weight_pct"]) for a in assets]
        top_sym, top_w = max(weights, key=lambda x: x[1])

        risk_score = round(top_w / 10, 2)
        risk_level = (
            "Düşük"   if top_w < 30  else
            "Orta"    if top_w < 55  else
            "Yüksek"  if top_w < 80  else
            "Çok Yüksek"
        )

        warnings: list[str] = []
        if self._detector and state.positions:
            for w in self._detector.check_portfolio_health(state):
                warnings.append(w.title)

        return {
            "risk_score":              risk_score,
            "risk_level":              risk_level,
            "max_concentration_pct":   round(top_w, 1),
            "max_concentration_asset": top_sym,
            "asset_count":             len(assets),
            "warnings":                warnings,
        }

    def _build_learning(self, ls: "LearningManager") -> dict:
        active_task = None
        for lvl in ls.levels:
            if not lvl.is_unlocked(ls.xp):
                continue
            t = lvl.get_next_task(ls._completed_tasks)
            if t:
                active_task = t
                break

        completed_count = len(ls._completed_tasks)
        total_count     = sum(l.total_task_count() for l in ls.levels)

        return {
            "current_level":          ls.current_level_label,
            "current_level_id":       ls.current_level,
            "xp":                     ls.xp,
            "current_task":           active_task.title     if active_task else None,
            "current_task_id":        active_task.id        if active_task else None,
            "current_task_objective": active_task.objective if active_task else None,
            "current_task_hint":      active_task.hint      if active_task else None,
            "tasks_completed":        completed_count,
            "tasks_total":            total_count,
        }

    def _build_leaderboard(
        self, lb: "LeaderboardManager", ls: "LearningManager"
    ) -> dict:
        rank    = lb.current_rank()
        entry   = lb.current_entry()
        top10   = lb.get_top_10()
        return {
            "username":    lb.username,
            "rank":        rank,
            "total_users": lb.entry_count,
            "session_pnl": entry.total_pnl if entry else None,
            "session_xp":  ls.xp,
            "top_pnl":     top10[0].total_pnl if top10 else None,
        }
