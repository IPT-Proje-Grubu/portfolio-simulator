from __future__ import annotations

from dataclasses import dataclass

from src.ui.i18n import lang_manager


ALERT_UP_THRESHOLD = 0.05
ALERT_DOWN_THRESHOLD = -0.03


@dataclass
class Alert:
    message: str
    level: str


def build_price_alert(symbol: str, projected_return: float) -> Alert | None:
    if projected_return >= ALERT_UP_THRESHOLD:
        return Alert(
            message=lang_manager.tr("UYARI: {symbol} %{val:.1f} artis sinirina ulasti.").format(symbol=symbol, val=projected_return * 100),
            level="success",
        )

    if projected_return <= ALERT_DOWN_THRESHOLD:
        return Alert(
            message=lang_manager.tr("UYARI: {symbol} %{val:.1f} dusus sinirina ulasti.").format(symbol=symbol, val=abs(projected_return) * 100),
            level="danger",
        )

    return None


def build_stable_alert() -> Alert:
    return Alert(
        message=lang_manager.tr("Uyari yok. Portfoy esikleri stabil gorunuyor."),
        level="info",
    )
