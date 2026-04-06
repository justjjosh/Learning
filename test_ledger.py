from decimal import Decimal
import pytest
from assignment_ledger import Side, Trade, Ledger


trade1 = Trade(
        trade_id = "T001",
        symbol = "BTC",
        side = Side.BUY,
        price = Decimal("15.00",),
        quantity = Decimal("10")
    )

trade2 = Trade(
        trade_id = "T002",
        symbol = "BTC",
        side = Side.BUY,
        price = Decimal("9.00",),
        quantity = Decimal("5")
    )
trade3 = Trade(
        trade_id = "T003",
        symbol = "BTC",
        side = Side.SELL,
        price = Decimal("7.50",),
        quantity = Decimal("3")
    )
trade4 = Trade(
        trade_id = "T004",
        symbol = "ETH",
        side = Side.SELL,
        price = Decimal("9.50",),
        quantity = Decimal("3")
    )

def test_add_trade():
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    assert len(book) == 2

def test_add_trade_duplicate_rejection():
    book = Ledger()
    book.add_trade(trade1)
    with pytest.raises(ValueError, match="Trade already exist"):
        book.add_trade(trade1)

def test_get_position_single_buy():
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    book.add_trade(trade3)
    assert book.get_position("BTC") == Decimal("12")

def test_get_position_buy_and_sell():
    book = Ledger()
    book.add_trade(trade1) # BUY 10
    book.add_trade(trade3) # SELL 3
    # ASSERT: 10 - 3 = 7
    assert book.get_position("BTC") == Decimal("7")

def test_get_position_nonexistent_symbol():
        book = Ledger()
        assert book.get_position("ETH") == Decimal("0")

def test_get_trades_by_symbol():
    # Add trades for multiple symbols, filter by one symbol
    book = Ledger()
    book.add_trade(trade3)
    book.add_trade(trade2)
    book.add_trade(trade4)
    btc_trades = book.get_trade_by_symbol("BTC")
    assert len(btc_trades) == 2
    for trade in btc_trades:
        assert trade.symbol == "BTC"

    
def test_get_trades_by_side():
    # Add BUY and SELL trades, filter by side
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    book.add_trade(trade4)
    assert len(book.get_trade_by_side(Side.BUY)) == 2
    assert trade1 in book.get_trade_by_side(Side.BUY)
    assert trade2 in book.get_trade_by_side(Side.BUY)

    
def test_get_notional_exposure():
    # Verify sum of notional values
    book = Ledger()
    book.add_trade(trade1)
    assert book.get_notional_exposure("BTC") == Decimal("150")
    
def test_len_magic_method():
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    assert len(book) == 2
    
def test_contains_magic_method():
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    book.add_trade(trade3)
    assert "T001" in book
    assert "T005" not in book
    # Verify "trade_id" in ledger works
    
def test_iter_magic_method():
    book = Ledger()
    book.add_trade(trade1)
    book.add_trade(trade2)
    book.add_trade(trade3)

    trade_count = 0
    for trade in book:
        trade_count += 1
    assert trade_count == 3

def test_repr_magic_method():
    book = Ledger()
    book.add_trade(trade1)
    output = repr(book)
    assert "Ledger:" in output
    assert "Unique symbol:" in output
    # Verify str(ledger) shows useful output

