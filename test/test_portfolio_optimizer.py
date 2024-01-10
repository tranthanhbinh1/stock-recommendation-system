import unittest
import pandas as pd
from portfolio_optimizer import PortfolioOptimizer

class TestPortfolioOptimizer(unittest.TestCase):
    def setUp(self):
        # Create a sample recommended stocks DataFrame
        self.recommended_stocks = pd.DataFrame({
            "stock": ["AAPL", "GOOGL", "AMZN", "MSFT", "FB"],
            "return": [0.1, 0.2, 0.15, 0.12, 0.18],
            "risk": [0.2, 0.15, 0.25, 0.18, 0.22]
        })

    def test_init(self):
        # Test the initialization of PortfolioOptimizer
        portfolio_optimizer = PortfolioOptimizer(self.recommended_stocks)
        self.assertEqual(portfolio_optimizer.recommended_stocks, self.recommended_stocks)
        self.assertEqual(portfolio_optimizer.portfolio_size, 3)
        self.assertEqual(portfolio_optimizer.risk_free_rate, 0.02)
        self.assertIsNone(portfolio_optimizer.upper_bound)
        self.assertEqual(portfolio_optimizer.top_stocks, [])

    def test_init_with_parameters(self):
        # Test the initialization of PortfolioOptimizer with custom parameters
        portfolio_optimizer = PortfolioOptimizer(
            self.recommended_stocks,
            portfolio_size=5,
            risk_free_rate=0.03,
            upper_bound=0.35
        )
        self.assertEqual(portfolio_optimizer.recommended_stocks, self.recommended_stocks)
        self.assertEqual(portfolio_optimizer.portfolio_size, 5)
        self.assertEqual(portfolio_optimizer.risk_free_rate, 0.03)
        self.assertEqual(portfolio_optimizer.upper_bound, 0.35)
        self.assertEqual(portfolio_optimizer.top_stocks, [])

    def test_set_top_stocks(self):
        # Test setting the top stocks in PortfolioOptimizer
        portfolio_optimizer = PortfolioOptimizer(self.recommended_stocks)
        top_stocks = ["AAPL", "GOOGL", "AMZN"]
        portfolio_optimizer.set_top_stocks(top_stocks)
        self.assertEqual(portfolio_optimizer.top_stocks, top_stocks)

if __name__ == '__main__':
    unittest.main()