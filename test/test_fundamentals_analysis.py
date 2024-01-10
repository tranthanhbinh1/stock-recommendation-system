import unittest
import pandas as pd
from fundamentals_analysis import FundamentalAnalysis

class TestFundamentalAnalysis(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        data = {
            "symbol": ["ABC", "DEF", "GHI"],
            "quarter": ["Q1 2022", "Q2 2022", "Q3 2022"],
            "eps_growth(%)": [10, 20, 30],
            "eps_(vnd)": [100, 200, 300],
            "revenue_growth_(%)": [15, 25, 35],
            "profit_growth_(%)": [5, 15, 25],
            "roe_(%)": [10, 20, 30]
        }
        self.df_fundamental = pd.DataFrame(data)
        self.latest_year = "2022"
        self.latest_quarter = "Q3 2022"
        self.recent_2_quarters = ["Q2 2022", "Q3 2022"]
        self.recent_3_quarters = ["Q1 2022", "Q2 2022", "Q3 2022"]
        self.growth_threshold_eps = 15
        self.growth_threshold_revenue = 20
        self.growth_threshold_roe = 15

    def test_check_eps_growth_1stcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.latest_quarter = self.latest_quarter
        fa.growth_threshold_eps = self.growth_threshold_eps

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_1": [True]
        })

        result = fa.check_eps_growth_1stcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_check_eps_growth_2ndcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.recent_2_quarters = self.recent_2_quarters
        fa.growth_threshold_eps = self.growth_threshold_eps

        expected_result = pd.DataFrame({
            "symbol": ["DEF", "GHI"],
            "condition_2": [True, True]
        })

        result = fa.check_eps_growth_2ndcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_assess_eps_near_peak_3rdcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.latest_year = self.latest_year

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_3": [True]
        })

        result = fa.assess_eps_near_peak_3rdcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_check_revenue_growth_4thcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.latest_quarter = self.latest_quarter
        fa.growth_threshold_revenue = self.growth_threshold_revenue

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_4": [True]
        })

        result = fa.check_revenue_growth_4thcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_check_accelerating_revenue_growth_5thcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.recent_3_quarters = self.recent_3_quarters

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_5": [True]
        })

        result = fa.check_accelerating_revenue_growth_5thcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_check_accelerating_profit_growth_6thcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.recent_3_quarters = self.recent_3_quarters

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_6": [True]
        })

        result = fa.check_accelerating_profit_growth_6thcondition()
        pd.testing.assert_frame_equal(result, expected_result)

    def test_check_roe_7thcondition(self):
        fa = FundamentalAnalysis()
        fa.df_fundamental = self.df_fundamental
        fa.latest_quarter = self.latest_quarter
        fa.growth_threshold_roe = self.growth_threshold_roe

        expected_result = pd.DataFrame({
            "symbol": ["GHI"],
            "condition_7": [True]
        })

        result = fa.check_roe_7thcondition()
        pd.testing.assert_frame_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()