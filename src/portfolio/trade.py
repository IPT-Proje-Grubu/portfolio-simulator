"""Trade dataclass — represents a single executed order."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    trade_id: int
    side: str        # "AL" | "SAT"
    symbol: str
    quantity: float
    price: float
    total: float
    timestamp: str

    @classmethod
    def new(
        cls,
        trade_id: int,
        side: str,
        symbol: str,
        quantity: float,
        price: float,
    ) -> "Trade":
        return cls(
            trade_id=trade_id,
            side=side,
            symbol=symbol,
            quantity=quantity,
            price=price,
            total=round(quantity * price, 2),
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        )
