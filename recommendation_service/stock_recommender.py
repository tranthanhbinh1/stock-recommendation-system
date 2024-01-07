import pandas as pd
import logging
from .fundamentals_analysis import FundamentalAnalysis
from .technical_analysis import TechnicalAnalysis
from utils.timescale_connector import TimescaleConnector
from utils.utils import filter_financial_ratio
from config.logging_config import setup_logging

setup_logging()
logging.getLogger(__name__)


class StockRecommender:
    def __init__(
        self,
        latest_year: str,
        latest_quarter: str,
        recent_2_quarters: list[str],
        recent_3_quarters: list[str],
        growth_threshold_eps: int,
        growth_threshold_revenue: int,
        growth_threshold_roe: int,
    ):
        self.latest_year = latest_year
        self.latest_quarter = latest_quarter
        self.recent_2_quarters = recent_2_quarters
        self.recent_3_quarters = recent_3_quarters
        self.growth_threshold_eps = growth_threshold_eps
        self.growth_threshold_revenue = growth_threshold_revenue
        self.growth_threshold_roe = growth_threshold_roe
        self.daily_price: pd.DataFrame = TimescaleConnector.query_ohlcv_all()
        self.financial_ratios: pd.DataFrame = filter_financial_ratio(
            TimescaleConnector.query_financial_ratios()
        )
        self.fundamental = FundamentalAnalysis(
            df_fundamental=self.financial_ratios,
            latest_year=self.latest_year,
            latest_quarter=self.latest_quarter,
            recent_2_quarters=self.recent_2_quarters,
            recent_3_quarters=self.recent_3_quarters,
            growth_threshold_eps=self.growth_threshold_eps,
            growth_threshold_revenue=self.growth_threshold_revenue,
            growth_threshold_roe=self.growth_threshold_roe,
        )
        self.technical = TechnicalAnalysis(df_technical=self.daily_price)

    # fmt: off
    def get_recommendation(self):
        logging.info("Checking EPS growth for the most recent quarter")
        condition_1 = self.fundamental.check_eps_growth_1stcondition().set_index("symbol")
        logging.info("Checking EPS growth for the two most recent quarters")
        condition_2 = self.fundamental.check_eps_growth_2ndcondition()
        logging.info("Checking EPS growth for the last 12 months")
        condition_3 = self.fundamental.assess_eps_near_peak_3rdcondition()
        logging.info("Checking revenue growth for the most recent quarter")
        condition_4 = self.fundamental.check_revenue_growth_4thcondition().set_index("symbol")
        logging.info("Checking revenue growth for the two most recent quarters")
        condition_5 = self.fundamental.check_accelerating_revenue_growth_5thcondition()
        logging.info("Checking profit growth for the most recent quarter")
        condition_6 = self.fundamental.check_accelerating_profit_growth_6thcondition()
        logging.info("Checking ROE for the most recent quarter")    
        condition_7 = self.fundamental.check_roe_7thcondition().set_index("symbol")
        logging.info("Checking EMA34-89")
        condition_8 = self.technical.check_emacross_8thcondition()
        logging.info("Checking MA50-150-200")
        condition_9 = self.technical.check_ma_9thcondition()

        combined = pd.concat(
            [
                condition_1,
                condition_2,
                condition_3,
                condition_4,
                condition_5,
                condition_6,
                condition_7,
                condition_8,
                condition_9,
            ],
            axis=1,
        )
        combined["Total_Conditions_Met"] = combined.sum(axis=1)

        stocks_ranked = combined.sort_values(by="Total_Conditions_Met", ascending=False)
        stocks_ranked["Ranking"] = (
            stocks_ranked["Total_Conditions_Met"]
            .rank(ascending=False, method="first")
            .astype(int)
        )
        # Rank the stocks based on the number of conditions met

        return stocks_ranked
