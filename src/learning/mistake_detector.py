"""Rule-based mistake detection — Learn by Failing.

Each rule inspects portfolio state before/after an action and returns a
MistakeWarning if a poor decision is detected.  Warnings are designed to be
short, educational, and actionable — NOT long essays.

Severity levels:
  "info"    — neutral tip (blue)
  "warning" — concerning but recoverable (amber)
  "danger"  — significant risk taken (red)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MistakeWarning:
    """A single coaching message triggered by a risky user action."""

    severity:    str   # "info" | "warning" | "danger"
    icon:        str
    title:       str
    explanation: str   # WHY this is a problem (1 sentence)
    suggestion:  str   # What to do instead (1 sentence)

    @property
    def color(self) -> str:
        return {"info": "#2563eb", "warning": "#f59e0b", "danger": "#ef4444"}.get(self.severity, "#2563eb")


# ── Individual rule functions ─────────────────────────────────────────────────

def _rule_overconcentration(
    state: Any, symbol: str, trade_total: float
) -> MistakeWarning | None:
    """Warn when a single asset exceeds 70 % of portfolio after a buy."""
    pv = state.portfolio_value
    if pv <= 0:
        return None
    pos = next((p for p in state.positions if p.symbol == symbol), None)
    if not pos:
        return None
    weight = pos.market_value / pv * 100
    if weight >= 70:
        return MistakeWarning(
            severity="danger",
            icon="⚠️",
            title=f"{symbol} portföyün %{weight:.0f}'ini oluşturuyor",
            explanation="Tek bir varlığa bu kadar yoğunlaşmak, o varlığın düşüşünde büyük kayıp yaratır.",
            suggestion="Farklı sektörlerden 3+ varlık satın alarak riski dağıt.",
        )
    if weight >= 55:
        return MistakeWarning(
            severity="warning",
            icon="⚡",
            title=f"{symbol} ağırlığı yüksek (%{weight:.0f})",
            explanation="Portföyünün yarısından fazlası tek varlıkta; piyasa düşüşü sert etki yapar.",
            suggestion="Başka bir varlık ekleyerek %50'nin altına çekmeyi deneyin.",
        )
    return None


def _rule_large_single_trade(
    state: Any, trade_total: float, available_cash_before: float
) -> MistakeWarning | None:
    """Warn when a single buy consumes > 80 % of available cash."""
    if available_cash_before <= 0:
        return None
    pct = trade_total / available_cash_before * 100
    if pct >= 80:
        return MistakeWarning(
            severity="warning",
            icon="💸",
            title=f"Nakitin %{pct:.0f}'ini tek hamlede harcadınız",
            explanation="Tüm nakit tek işlemde kullanılırsa fırsat çıktığında alım yapacak para kalmaz.",
            suggestion="Nakitin en fazla %50'sini tek seferde kullan; geri kalanını fırsatlar için sakla.",
        )
    return None


def _rule_panic_sell_at_loss(
    state: Any, symbol: str, sell_price: float, avg_cost: float
) -> MistakeWarning | None:
    """Warn when selling at a large loss while the asset might recover."""
    if avg_cost <= 0:
        return None
    loss_pct = (sell_price - avg_cost) / avg_cost * 100
    if loss_pct <= -25:
        return MistakeWarning(
            severity="warning",
            icon="📉",
            title=f"{symbol}: %{abs(loss_pct):.0f} zararda satış",
            explanation="Panikle satış, kağıt üzerindeki kaybı gerçek kayba dönüştürür.",
            suggestion="Fiyatın neden düştüğünü analiz et; uzun vadeli varlıklar genellikle toparlanır.",
        )
    return None


def _rule_selling_winner_early(
    state: Any, symbol: str, sell_price: float, avg_cost: float
) -> MistakeWarning | None:
    """Hint when selling a strongly rising asset — might be premature."""
    if avg_cost <= 0:
        return None
    gain_pct = (sell_price - avg_cost) / avg_cost * 100
    if gain_pct >= 40:
        return MistakeWarning(
            severity="info",
            icon="💡",
            title=f"{symbol} güçlü yükseliş trendinde (+%{gain_pct:.0f})",
            explanation="Yükseliş trendi devam edebilir; erken satış ek kazançları kaçırmana yol açabilir.",
            suggestion="Pozisyonun yarısını sat, geri kalanı ile trend takibini sürdür.",
        )
    return None


def _rule_no_diversification(state: Any) -> MistakeWarning | None:
    """Warn when the user has done many trades but still holds only 1 asset."""
    if len(state.trade_history) >= 5 and len(state.positions) <= 1:
        return MistakeWarning(
            severity="warning",
            icon="🌐",
            title="5+ işlem, hâlâ tek varlık",
            explanation="Birden fazla işlem yaptın ama çeşitlendirme yapmadın; tek varlık riski devam ediyor.",
            suggestion="BTC'ye ek olarak ETH, AAPL veya GOLD gibi farklı sektörlerden bir varlık al.",
        )
    return None


def _rule_idle_cash(state: Any) -> MistakeWarning | None:
    """Hint when > 90 % of portfolio is idle cash after multiple trades."""
    pv = state.portfolio_value
    if pv <= 0 or len(state.trade_history) < 3:
        return None
    cash_pct = state.cash / pv * 100
    if cash_pct >= 90:
        return MistakeWarning(
            severity="info",
            icon="😴",
            title=f"Nakitin %{cash_pct:.0f}'i atıl duruyor",
            explanation="Portföyünün büyük kısmı nakit; yatırım yapmadan kâr edilemez.",
            suggestion="Piyasayı incele ve nakdinin bir kısmını çeşitlendirilmiş varlıklara yatır.",
        )
    return None


def _rule_over_trading(state: Any) -> MistakeWarning | None:
    """Warn when trade count grows very high without profit."""
    if len(state.trade_history) >= 20 and state.total_realized_pnl < 0:
        return MistakeWarning(
            severity="warning",
            icon="🔄",
            title="Çok fazla işlem, zarar büyüyor",
            explanation="20+ işleme rağmen gerçekleşmiş kâr negatif; sürekli alım-satım sorunu çözmez.",
            suggestion="Strateji belirle: bir varlığı hedef fiyata kadar tut, ardından sat.",
        )
    return None


# ── MistakeDetector ───────────────────────────────────────────────────────────

class MistakeDetector:
    """
    Rule-based detector that returns coaching warnings for risky trading actions.

    Usage
    -----
    detector = MistakeDetector()

    # Before executing a buy, capture available cash:
    cash_before = state.cash

    # After executing:
    warnings = detector.check_after_buy(state, symbol, trade_total, cash_before)
    warnings += detector.check_portfolio_health(state)

    # After executing a sell:
    warnings = detector.check_after_sell(state, symbol, sell_price, avg_cost_before_sell)
    """

    def check_after_buy(
        self,
        state: Any,
        symbol: str,
        trade_total: float,
        cash_before: float,
    ) -> list[MistakeWarning]:
        warnings: list[MistakeWarning] = []
        w = _rule_overconcentration(state, symbol, trade_total)
        if w:
            warnings.append(w)
        w = _rule_large_single_trade(state, trade_total, cash_before)
        if w:
            warnings.append(w)
        return warnings

    def check_after_sell(
        self,
        state: Any,
        symbol: str,
        sell_price: float,
        avg_cost_before_sell: float,
    ) -> list[MistakeWarning]:
        warnings: list[MistakeWarning] = []
        w = _rule_panic_sell_at_loss(state, symbol, sell_price, avg_cost_before_sell)
        if w:
            warnings.append(w)
        w = _rule_selling_winner_early(state, symbol, sell_price, avg_cost_before_sell)
        if w:
            warnings.append(w)
        return warnings

    def check_portfolio_health(self, state: Any) -> list[MistakeWarning]:
        """Periodic health check — call after every significant action."""
        warnings: list[MistakeWarning] = []
        for rule_fn in (_rule_no_diversification, _rule_idle_cash, _rule_over_trading):
            w = rule_fn(state)
            if w:
                warnings.append(w)
        return warnings
