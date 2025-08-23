# accounts.py

class Account:
    SHARE_PRICES = {
        "AAPL": 150.0,
        "TSLA": 600.0,
        "GOOGL": 2800.0
    }

    def __init__(self, initial_deposit: float = 0.0) -> None:
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(("DEPOSIT", amount))

    def withdraw(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(("WITHDRAWAL", amount))
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = self._get_share_price(symbol)
        total_cost = price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append(("BUY", symbol, quantity, price))
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if self.holdings.get(symbol, 0) >= quantity:
            price = self._get_share_price(symbol)
            total_sale = price * quantity
            self.balance += total_sale
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append(("SELL", symbol, quantity, price))
            return True
        return False

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += quantity * self._get_share_price(symbol)
        return total_value

    def get_profit_or_loss(self) -> float:
        current_value = self.get_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return dict(self.holdings)

    def list_transactions(self) -> list:
        return list(self.transactions)

    def _get_share_price(self, symbol: str) -> float:
        return self.SHARE_PRICES.get(symbol, 0.0)