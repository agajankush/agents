`import unittest

# Assuming accounts.py is accessible
from accounts import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        """Set up a test account for each test method."""
        self.account = Account(initial_deposit=1000.0)

    def test_initialization(self):
        """Test account initialization."""
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        """Test depositing amount increases balance."""
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertIn(("DEPOSIT", 500.0), self.account.transactions)

    def test_withdraw(self):
        """Test withdrawal processing."""
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)
        self.assertIn(("WITHDRAWAL", 200.0), self.account.transactions)

        # Test insufficient funds
        result = self.account.withdraw(1200.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 800.0)  # Balance should be unchanged

    def test_buy_shares(self):
        """Test buying shares reduces balance and updates holdings."""
        result = self.account.buy_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.holdings.get("AAPL"), 5)
        self.assertIn(("BUY", "AAPL", 5, 150.0), self.account.transactions)

        # Test insufficient balance to buy shares
        result = self.account.buy_shares("TSLA", 10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 250.0)  # Balance should be unchanged
        self.assertNotIn(("BUY", "TSLA", 10, 600.0), self.account.transactions)

    def test_sell_shares(self):
        """Test selling shares increases balance and updates holdings."""
        self.account.buy_shares("AAPL", 5)
        result = self.account.sell_shares("AAPL", 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.holdings.get("AAPL"), 2)
        self.assertIn(("SELL", "AAPL", 3, 150.0), self.account.transactions)

        # Test cannot sell more shares than owned
        result = self.account.sell_shares("AAPL", 10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 700.0)

    def test_get_portfolio_value(self):
        """Test calculation of portfolio value."""
        self.account.buy_shares("TSLA", 1)
        portfolio_value = self.account.get_portfolio_value()
        self.assertEqual(portfolio_value, 1000)

    def test_get_profit_or_loss(self):
        """Test profit or loss calculation relative to initial deposit."""
        profit_or_loss = self.account.get_profit_or_loss()
        self.assertEqual(profit_or_loss, 0.0)

        # Simulate buy/sell shares to modify profit/loss
        self.account.buy_shares("TSLA", 1)
        self.account.sell_shares("TSLA", 1)
        updated_profit_or_loss = self.account.get_profit_or_loss()
        self.assertEqual(updated_profit_or_loss, 0.0)  # No real gain or loss

    def test_get_holdings(self):
        """Test getting a copy of holdings."""
        self.account.buy_shares("GOOGL", 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"GOOGL": 2})

    def test_list_transactions(self):
        """Test listing all transactions."""
        self.account.deposit(100)
        self.account.withdraw(50)
        transactions = self.account.list_transactions()
        expected_transactions = [
            ("DEPOSIT", 100),
            ("WITHDRAWAL", 50)
        ]
        self.assertEqual(transactions, expected_transactions)

if __name__ == '__main__':
    unittest.main()`