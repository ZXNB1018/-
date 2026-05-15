"""Simple MVP strategy module."""
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Signal:
    symbol: str
    side: str
    confidence: float


def sma(values: Sequence[float], window: int) -> float:
    if window <= 0:
        raise ValueError("window must be positive")
    if len(values) < window:
        raise ValueError("insufficient data for SMA window")
    chunk = values[-window:]
    return sum(chunk) / window


def generate_signal(symbol: str, closes: Sequence[float], fast_window: int, slow_window: int) -> Signal:
    """Generate a long/flat signal with simple moving-average crossover."""
    fast = sma(closes, fast_window)
    slow = sma(closes, slow_window)
    if fast > slow:
        return Signal(symbol=symbol, side="BUY", confidence=min((fast - slow) / slow, 1.0))
    return Signal(symbol=symbol, side="HOLD", confidence=min((slow - fast) / slow, 1.0))
