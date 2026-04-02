from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field
from decimal import Decimal

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass(frozen=True)
class Trade:
    trade_id: str
    symbol: str
    side: Side
    price: Decimal
    quantity: Decimal
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.price <= 0 or self.quantity <= 0:
            raise ValueError("Invaid input")
        
    @property
    def notional_value(self) -> Decimal:
        return self.price * self.quantity
    
class Ledger:
    def __init__(self) -> None:
        self._trades: set[Trade] = set()
        self._trade_by_ids: set[str] = set()

    def add_trade(self, trade: Trade) -> None:
        if trade.trade_id in self._trade_by_ids:
            raise ValueError("Trade already exist")
        self._trade_by_ids.add(trade.trade_id)
        self._trades.add(trade)
    
    """def add_trade_by_id(self, trade: Trade) -> None:
        if trade.trade_id in self._trade_by_ids:
            raise ValueError("Trade already exist")
        self._trades.add(trade)
        self._trade_by_ids(trade)"""
    
    def get_trade_by_symbol(self, symbol: str) -> list[Trade]:
        trade_by_symbol = []
        for trade in self._trades:
            if trade.symbol == symbol:
                trade_by_symbol.append(trade)
        return sorted(trade_by_symbol, key=lambda trade: trade.executed_at, reverse=True)
    
    def get_trade_by_side(self, side: Side) -> list[Trade]:
        trade_by_side = []
        for trade in self._trades:
            if trade.side == side:
                trade_by_side.append(trade)
        return sorted(trade_by_side, key=lambda trade: trade.executed_at, reverse=True)
    
    def get_position(self, symbol: str) -> Decimal:
        position = Decimal("0")
        for trade in self._trades:
            if trade.symbol == symbol:
                if trade.side == Side.BUY:
                    position += trade.quantity
                elif trade.side == Side.SELL:
                    position -= trade.quantity
        return position
    
    def get_notional_exposure(self, symbol: str) -> Decimal:
        notional_by_symbol = Decimal("0")
        found_symbol = False
        for trade in self._trades:
            if trade.symbol == symbol:
                notional_by_symbol += trade.price * trade.quantity
                found_symbol = True
        if not found_symbol:
            raise ValueError(f"{symbol} not found in Ledger")
        return notional_by_symbol
    
    def total_trades(self) -> int:
        return len(self._trades)
    
    @property
    def get_trades(self)-> list[Trade]:
        return list(self._trades)
    
    def __len__(self) -> int:
        return len(self._trades)
    
    def __contains__(self, trade_id: str) -> bool:
        return trade_id in self._trade_by_ids
    
    def __iter__(self):
        return iter(self._trades)

    def __repr__(self):
        unique_symbols = ({trade.symbol for trade in self._trades})
        return f"Ledger: {len(self._trades)}, Unique symbol: {unique_symbols}"
    
trade_1 = Trade(
    trade_id="T-001",
    symbol="BTC-USD",
    side=Side.BUY,
    quantity=Decimal("15.0"),
    price=Decimal("52000.25"),
)
trade_2 = Trade(
    trade_id="T-002",
    symbol="BTC-USD",
    side=Side.SELL,
    quantity=Decimal("5.0"),
    price=Decimal("52000.25"),
)

ledger = Ledger()
ledger.add_trade(trade_1)
#ledger.add_trade(trade_2)
