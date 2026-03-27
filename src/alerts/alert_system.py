from __future__ import annotations

from dataclasses import dataclass


ALERT_UP_THRESHOLD = 0.05
ALERT_DOWN_THRESHOLD = -0.03


@dataclass
class Alert:
    message: str
    level: str


def build_price_alert(symbol: str, projected_return: float) -> Alert | None:
    if projected_return >= ALERT_UP_THRESHOLD:
        return Alert(
            message=f"UYARI: {symbol} %{projected_return * 100:.1f} artis sinirina ulasti.",
            level="success",
        )

    if projected_return <= ALERT_DOWN_THRESHOLD:
        return Alert(
            message=f"UYARI: {symbol} %{abs(projected_return) * 100:.1f} dusus sinirina ulasti.",
            level="danger",
        )

    return None


def build_stable_alert() -> Alert:
    return Alert(
        message="Uyari yok. Portfoy esikleri stabil gorunuyor.",
        level="info",
    )
