import pandas as pd
import numpy as np
import logging
from functools import lru_cache
from typing import Union
from scipy.optimize import minimize
from utils.timescale_connector import TimescaleConnector
from config.logging_config import setup_logging

setup_logging()
logging.getLogger(__name__)


class PortfolioOptimizer:
    def __init__(
        self,
        recommended_stocks: pd.DataFrame,
        portfolio_size: Union[3, 5] = 3,
        risk_free_rate: float = 0.02,
        upper_bound: Union[0.5, 0.35, 0.25] = None, # Equals to: High Risk, Medium Risk, Low Risk
    ):
        self.recommended_stocks = recommended_stocks
        self.portfolio_size = portfolio_size
        self.risk_free_rate = risk_free_rate
        self.upper_bound = upper_bound
        self.top_stocks: list = []

    @lru_cache(maxsize=2)  # 3 and 5 best stocks
    def get_top_stocks(self) -> None:
        recommended_stocks = self.recommended_stocks
        self.top_stocks = recommended_stocks.head(self.portfolio_size).index.tolist()
        logging.info(f"Top {self.portfolio_size} stocks: {self.top_stocks}")

    def query_stock_prices(self) -> None:
        for symbol in self.top_stocks:
            df = TimescaleConnector.query_ohlcv_daily(symbol)
            df = df.close
            df.columns = [symbol]
            if symbol == self.top_stocks[0]:
                self.top_stocks_df = df
            else:
                self.top_stocks_df = pd.concat([self.top_stocks_df, df], axis=1)

    def calculate_log_returns(self) -> None:
        self.top_stocks_df = self.top_stocks_df.astype(float)
        self.log_returns = np.log(
            self.top_stocks_df / self.top_stocks_df.shift(1)
        ).dropna()

    def calculate_covariance_matrix(self) -> None:
        self.cov_matrix_annual = self.log_returns.cov() * 252

    def standard_deviation(self, weights) -> float:
        variance = weights.T @ self.cov_matrix_annual @ weights
        return np.sqrt(variance)

    def expected_return(self, weights) -> float:
        return np.sum(self.log_returns.mean() * weights) * 252

    def sharpe_ratio(self, weights, risk_free_rate) -> float:
        return (
            self.expected_return(weights) - risk_free_rate
        ) / self.standard_deviation(weights)

    def optimize_portfolio(self) -> None:
        constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
        bounds = [(0, self.upper_bound) for _ in range(len(self.top_stocks))]
        initial_weights = np.array([1 / len(self.top_stocks)] * len(self.top_stocks))
        optimized_results = minimize(
            self.sharpe_ratio,
            initial_weights,
            args=(self.risk_free_rate,),
            method="SLSQP",
            constraints=constraints,
            bounds=bounds,
        )
        self.optimal_weights = optimized_results.x

    def get_optimal_portfolio(self) -> None:
        optimal_portfolio = {}
        optimal_portfolio_return = self.expected_return(self.optimal_weights)
        optimal_portfolio_volatility = self.standard_deviation(self.optimal_weights)
        optimal_sharpe_ratio = self.sharpe_ratio(
            self.optimal_weights, risk_free_rate=0.02
        )

        logging.info("Optimal Weights:")
        for ticker, weight in zip(self.top_stocks, self.optimal_weights):
            optimal_portfolio[ticker] = weight
            logging.info(f"{ticker}: {weight:.4f}")

        logging.info(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
        logging.info(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
        logging.info(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")
        optimal_portfolio["Expected Annual Return"] = optimal_portfolio_return
        optimal_portfolio["Expected Volatility"] = optimal_portfolio_volatility
        optimal_portfolio["Sharpe Ratio"] = optimal_sharpe_ratio
        return optimal_portfolio


if __name__ == "__main__":
    optimizer = PortfolioOptimizer(portfolio_size=5, upper_bound=0.25)
    optimizer.get_top_stocks()
    optimizer.query_stock_prices()
    optimizer.calculate_log_returns()
    optimizer.calculate_covariance_matrix()
    optimizer.optimize_portfolio()
    optimizer.get_optimal_portfolio()
