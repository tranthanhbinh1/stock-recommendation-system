import pandas as pd
import warnings
from dataclasses import dataclass

warnings.filterwarnings("ignore")


@dataclass
class FundamentalAnalysis:
    df_fundamental: pd.DataFrame
    latest_year: str
    latest_quarter: str
    recent_2_quarters: list[str]
    recent_3_quarters: list[str]
    growth_threshold_eps: int
    growth_threshold_revenue: int
    growth_threshold_roe: int

    # The most recent quarter's EPS growth is greater than 15% compared to the same quarter of the previous year
    def check_eps_growth_1stcondition(self) -> pd.DataFrame:
        latest_quarter_df = self.df_fundamental[
            self.df_fundamental["quarter"] == self.latest_quarter
        ]
        latest_quarter_df["condition_1"] = (
            latest_quarter_df["eps_growth(%)"] > self.growth_threshold_eps
        )
        return latest_quarter_df[["symbol", "condition_1"]]

    # EPS growth for the two most recent quarters is greater than 15% compared to the same quarters of the previous year
    def check_eps_growth_2ndcondition(self) -> pd.DataFrame:
        recent_quarter_df = self.df_fundamental[
            self.df_fundamental["quarter"].isin(self.recent_2_quarters)
        ]
        result = recent_quarter_df.groupby("symbol").apply(
            lambda x: (x["eps_growth(%)"] > self.growth_threshold_eps).all()
        )
        # Set column name to: condition_2
        result.name = "condition_2"
        result.index.name = "symbol"
        return result

    # Earnings Per Share (EPS) in each quarter of the last 12 months is at or near its peak
    def assess_eps_near_peak_3rdcondition(self) -> pd.DataFrame:
        year_df = self.df_fundamental[
            self.df_fundamental["quarter"].str.contains(self.latest_year)
        ]

        def is_eps_at_peak(stock_df):
            max_eps = 0
            for eps in stock_df["eps_(vnd)"]:
                near_peak = max_eps * 0.95
                if eps < near_peak:
                    return False
                max_eps = max(max_eps, eps)
            return True

        result = year_df.groupby("symbol").apply(is_eps_at_peak)
        # Set column name to: condition_3
        result.name = "condition_3"
        result.index.name = "symbol"
        return result

    # Most recent quarter's revenue is greater than 20% compared to the same quarter of the previous year
    def check_revenue_growth_4thcondition(self) -> pd.DataFrame:
        latest_quarter_df = self.df_fundamental[
            self.df_fundamental["quarter"] == self.latest_quarter
        ]
        latest_quarter_df["condition_4"] = (
            latest_quarter_df["revenue_growth_(%)"] > self.growth_threshold_revenue
        )
        return latest_quarter_df[["symbol", "condition_4"]]

    # Accelerating revenue growth over the last three quarters
    def check_accelerating_revenue_growth_5thcondition(self) -> pd.DataFrame:
        filtered_df = self.df_fundamental[
            self.df_fundamental["quarter"].isin(self.recent_3_quarters)
        ]

        def is_growth_accelerating(stock_df) -> bool:
            stock_df = stock_df.sort_values(by="quarter")
            growth_rates = stock_df["revenue_growth_(%)"].tolist()
            return all(x < y for x, y in zip(growth_rates, growth_rates[1:]))

        result = filtered_df.groupby("symbol").apply(is_growth_accelerating)
        # Set column name to: condition_5
        result.name = "condition_5"
        result.index.name = "symbol"
        return result

    # Accelerating profit growth over the last three quarters
    def check_accelerating_profit_growth_6thcondition(self) -> pd.DataFrame:
        filtered_df = self.df_fundamental[
            self.df_fundamental["quarter"].isin(self.recent_3_quarters)
        ]

        def is_growth_accelerating(stock_df):
            stock_df = stock_df.sort_values(by="quarter")
            growth_rates = stock_df["profit_growth_(%)"].tolist()
            return all(x < y for x, y in zip(growth_rates, growth_rates[1:]))

        result = filtered_df.groupby("symbol").apply(is_growth_accelerating)
        # Set column name to: condition_6
        result.name = "condition_6"
        result.index.name = "symbol"
        return result

    # Return on Equity (ROE) in the most recent quarter is greater than 15 %
    def check_roe_7thcondition(self) -> pd.DataFrame:
        current_quarter_df = self.df_fundamental[
            self.df_fundamental["quarter"] == self.latest_quarter
        ]
        current_quarter_df["condition_7"] = (
            current_quarter_df["roe_(%)"] >= self.growth_threshold_roe
        )
        return current_quarter_df[["symbol", "condition_7"]]
