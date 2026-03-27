from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrendSummary:
    direction: str
    change_pct: float
    volatility_pct: float


class TrendAnalyzer:
    def summarize(self, series: list[float]) -> TrendSummary:
        if len(series) < 2:
            return TrendSummary(direction="not_enough_data", change_pct=0.0, volatility_pct=0.0)

        first_value = series[0]
        last_value = series[-1]
        change_pct = 0.0 if first_value == 0 else ((last_value - first_value) / first_value) * 100

        deltas = [abs(current - previous) for previous, current in zip(series, series[1:])]
        average_delta = sum(deltas) / len(deltas) if deltas else 0.0
        volatility_pct = 0.0 if first_value == 0 else (average_delta / first_value) * 100

        direction = "flat"
        if change_pct > 0.5:
            direction = "up"
        elif change_pct < -0.5:
            direction = "down"

        return TrendSummary(
            direction=direction,
            change_pct=round(change_pct, 2),
            volatility_pct=round(volatility_pct, 2),
        )
