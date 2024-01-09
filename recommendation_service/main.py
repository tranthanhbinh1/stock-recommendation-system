from .stock_recommender import StockRecommender
from .portfolio_optimizer import PortfolioOptimizer
from config.logging_config import setup_logging
import logging
import pandas as pd

setup_logging()
logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        stock_recommender: StockRecommender,
        portfolio_optimizer: PortfolioOptimizer,
    ):
        self.stock_recommender = stock_recommender
        self.portfolio_optimizer = portfolio_optimizer

    # TODO: add a Industry filter to the recommendation
    def get_ranked_stock(self):
        _df = self.stock_recommender.get_recommendation()
        ranking = pd.DataFrame(
            {
                "symbol": _df.index,
                "number_of_conditions_met": _df["Total_Conditions_Met"],
                "rank": _df["Ranking"],
            }
        ).reset_index(drop=True)
        ranking.to_csv("ranking.csv", index=False)

        return ranking

    def get_optimized_portfolio(self):
        self.portfolio_optimizer.get_top_stocks()
        self.portfolio_optimizer.query_stock_prices()
        self.portfolio_optimizer.calculate_log_returns()
        self.portfolio_optimizer.calculate_covariance_matrix()
        self.portfolio_optimizer.optimize_portfolio()
        return self.portfolio_optimizer.get_optimal_portfolio()


if __name__ == "__main__":
    stock_recommender = StockRecommender(
        latest_year="2023",
        latest_quarter="Q3 2023",
        recent_2_quarters=["Q3 2023", "Q2 2023"],
        recent_3_quarters=["Q1 2023", "Q2 2023", "Q3 2023"],
        growth_threshold_eps=15,
        growth_threshold_revenue=20,
        growth_threshold_roe=15,
        chosen_industries=["Dịch vụ tài chính", "Điện tử và thiết bị điện", "Phần mềm và dịch vụ máy tính"]
    )
    recommended_stocks = stock_recommender.get_recommendation()
    portfolio_optimizer = PortfolioOptimizer(
        recommended_stocks=recommended_stocks,
        portfolio_size=5,
        risk_free_rate=0.02,
        upper_bound=0.25,
    )
    recommendation_service = RecommendationService(
        stock_recommender, portfolio_optimizer
    )
    recommended_stock = recommendation_service.get_ranked_stock()
    optimal_portfolio = recommendation_service.get_optimized_portfolio()
    logging.info(recommended_stock)
    logging.info(optimal_portfolio)
