from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AllocationSlice:
    label: str
    value: float
    percentage: float


def build_allocation_slices(values: list[tuple[str, float]]) -> list[AllocationSlice]:
    total = sum(value for _, value in values) or 1.0
    return [
        AllocationSlice(
            label=label,
            value=value,
            percentage=round((value / total) * 100, 2),
        )
        for label, value in values
    ]
