"""Order request model used across agents."""
from dataclasses import dataclass


@dataclass
class OrderRequest:
    symbol: str
    side: str
    quantity: int
    order_type: str = "MARKET"
