from trading_agent.agents.signal_agent.strategy import generate_signal


def test_generate_signal_buy_on_fast_above_slow():
    closes = list(range(1, 100))
    signal = generate_signal("AAPL", closes, fast_window=5, slow_window=20)
    assert signal.side == "BUY"


def test_generate_signal_hold_on_fast_below_slow():
    closes = list(range(100, 0, -1))
    signal = generate_signal("AAPL", closes, fast_window=5, slow_window=20)
    assert signal.side == "HOLD"
