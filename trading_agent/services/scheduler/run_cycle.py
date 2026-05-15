"""Single-cycle orchestrator for the MVP paper-trading loop."""
from trading_agent.agents.signal_agent.strategy import generate_signal


def run_cycle(symbol: str, closes: list[float], fast_window: int = 20, slow_window: int = 60) -> dict:
    signal = generate_signal(symbol, closes, fast_window, slow_window)
    return {
        "symbol": signal.symbol,
        "side": signal.side,
        "confidence": round(signal.confidence, 4),
    }
