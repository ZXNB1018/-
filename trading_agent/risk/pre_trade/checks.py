"""Pre-trade risk checks for MVP."""
from dataclasses import dataclass


@dataclass
class RiskDecision:
    approved: bool
    reason: str


def check_max_position(target_position_value: float, nav: float, max_position_pct: float) -> RiskDecision:
    if nav <= 0:
        return RiskDecision(False, "Invalid NAV")
    if target_position_value / nav > max_position_pct:
        return RiskDecision(False, "Position exceeds max allocation")
    return RiskDecision(True, "Approved")
