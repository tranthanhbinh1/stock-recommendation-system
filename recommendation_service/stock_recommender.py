import pandas as pd
from .fundamentals_analysis import FundamentalAnalysis
from .technical_analysis import TechnicalAnalysis
from utils.timescale_connector import TimescaleConnector
from utils.utils import filter_financial_ratio


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

    def get_recommendation(self):
        condition_1 = self.fundamental.check_eps_growth_1stcondition().set_index("symbol")
        condition_2 = self.fundamental.check_eps_growth_2ndcondition()
        condition_3 = self.fundamental.assess_eps_near_peak_3rdcondition()
        condition_4 = self.fundamental.check_revenue_growth_4thcondition().set_index("symbol")
        condition_5 = self.fundamental.check_accelerating_revenue_growth_5thcondition()
        condition_6 = self.fundamental.check_accelerating_profit_growth_6thcondition()
        condition_7 = self.fundamental.check_roe_7thcondition().set_index("symbol")
        condition_8 = self.technical.check_emacross_8thcondition()
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
        combined["Total Conditions Met"] = combined.sum(axis=1)

        stocks_ranked = combined.sort_values(by="Total Conditions Met", ascending=False)
        stocks_ranked["Ranking"] = (
            stocks_ranked["Total Conditions Met"]
            .rank(ascending=False, method="first")
            .astype(int)
        )
        # Rank the stocks based on the number of conditions met

        return stocks_ranked
