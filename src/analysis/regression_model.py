from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ForecastPoint:
    index: int
    value: float


class RegressionForecaster:
    """Lightweight forecasting helper until sklearn is integrated."""

    def predict_next(self, series: list[float], steps: int = 3) -> list[ForecastPoint]:
        if steps <= 0:
            return []
        if not series:
            return [ForecastPoint(index=index, value=0.0) for index in range(steps)]

        if len(series) == 1:
            start_index = len(series)
            return [
                ForecastPoint(index=start_index + index, value=series[0])
                for index in range(steps)
            ]

        slope = (series[-1] - series[0]) / max(len(series) - 1, 1)
        start_index = len(series)
        base_value = series[-1]

        forecasts: list[ForecastPoint] = []
        for index in range(steps):
            next_value = base_value + slope * (index + 1)
            forecasts.append(
                ForecastPoint(index=start_index + index, value=round(next_value, 2))
            )

        return forecasts
