"""Simulated price feed for watchlist assets (used until real CSV data is loaded)."""

from __future__ import annotations

import random

WATCHLIST: dict[str, dict] = {
    "BTC":  {"name": "Bitcoin",        "price": 1_720_000.0, "vol": 0.014, "sector": "Kripto"},
    "ETH":  {"name": "Ethereum",       "price": 112_000.0,   "vol": 0.018, "sector": "Kripto"},
    "BNB":  {"name": "BNB",            "price": 19_500.0,    "vol": 0.016, "sector": "Kripto"},
    "SOL":  {"name": "Solana",         "price": 5_200.0,     "vol": 0.024, "sector": "Kripto"},
    "AAPL": {"name": "Apple Inc.",     "price": 6_100.0,     "vol": 0.008, "sector": "Hisse"},
    "MSFT": {"name": "Microsoft",      "price": 14_200.0,    "vol": 0.007, "sector": "Hisse"},
    "NVDA": {"name": "Nvidia",         "price": 47_500.0,    "vol": 0.022, "sector": "Hisse"},
    "TSLA": {"name": "Tesla",          "price": 8_600.0,     "vol": 0.026, "sector": "Hisse"},
    "GOOG": {"name": "Alphabet",       "price": 54_000.0,    "vol": 0.009, "sector": "Hisse"},
    "AMZN": {"name": "Amazon",         "price": 62_000.0,    "vol": 0.012, "sector": "Hisse"},
    "GOLD": {"name": "Altin (oz)",     "price": 62_500.0,    "vol": 0.004, "sector": "Emtia"},
    "BIST": {"name": "BIST 100",       "price": 9_850.0,     "vol": 0.011, "sector": "Endeks"},
}


class PriceFeed:
    """Random-walk price feed.  tick() advances one step."""

    def __init__(self) -> None:
        self._prices: dict[str, float] = {
            sym: float(info["price"]) for sym, info in WATCHLIST.items()
        }
        self._prev: dict[str, float] = dict(self._prices)
        self._open: dict[str, float] = dict(self._prices)

    def tick(self) -> dict[str, float]:
        self._prev = dict(self._prices)
        for sym, info in WATCHLIST.items():
            drift = random.gauss(0.0001, info["vol"] / 14)
            self._prices[sym] = max(round(self._prices[sym] * (1.0 + drift), 2), 1.0)
        return dict(self._prices)

    def get_all(self) -> dict[str, float]:
        return dict(self._prices)

    def get_price(self, symbol: str) -> float:
        return self._prices.get(symbol.upper(), 0.0)

    def change_pct(self, symbol: str) -> float:
        curr = self._prices.get(symbol, 0.0)
        prev = self._prev.get(symbol, curr)
        return 0.0 if prev == 0 else (curr - prev) / prev * 100

    def day_change_pct(self, symbol: str) -> float:
        curr = self._prices.get(symbol, 0.0)
        opn  = self._open.get(symbol, curr)
        return 0.0 if opn == 0 else (curr - opn) / opn * 100
