from decimal import Decimal
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass(frozen=True) #makes the class imutable
class Trade:
    trade_id: str
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    executed_at: datetime =  datetime.now(timezone.utc)

    def __post_init__(self): #Let's you set a conditional statement
        if self.quantity <= 0 or self.price <= 0:
            raise ValueError (f"invalid input, {self.quantity} or {self.price} cannot be negative.")
        
    @property #notional(quantity * price) property decorator
    def notional_value(self)-> Decimal:
        return self.quantity * self.price
    
class Ledger:
    def __init__(self):
        self._trades: set[Trade] = set()
        self._seen_trade_ids: set[str] = set()


    def add_trade(self, trade: Trade)-> None:
        if trade.trade_id in self._seen_trade_ids:
            raise ValueError("Trade already exists")
        self._seen_trade_ids.add(trade.trade_id)
        self._trades.add(trade)

    def get_position(self, symbol: str) -> Decimal:
        position = Decimal("0")
        for trade in self.trades:
            if trade.symbol == symbol:
                if trade.side == Side.BUY:
                    position += trade.quantity
                elif trade.side == Side.SELL:
                    position -= trade.quantity
        return position
    
    def __len__(self) -> int:
        return len(self._trades)
    
    def __contains__(self, trade: str) -> bool:
        return trade in self._seen_trade_ids
    
    def __iter__(self):
        return iter(self._trades)
    
    def __repr__(self) -> str:
        unique_symbols = {trade.symbol for trade in self._trades}
        return f"Ledger(trades = {len(self._trades)}, unique_symbols = {len(unique_symbols)})"

                


    @property
    def trades(self)-> list[Trade]:
        return list(self._trades)
    

my_trade = Trade(
    trade_id="T-000",
    symbol="BTC-USD",
    side=Side.BUY,
    quantity=Decimal("20.0"),
    price=Decimal("52000.25"),
)
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
ledger.add_trade(trade_2)
ledger.add_trade(my_trade)

#Test magic methods
print(len(ledger))
print(f"{'T-001' in ledger}")
print("All trades")
for trade in ledger:
    print(f"{trade.trade_id}: {trade.side.value} {trade.quantity}")

