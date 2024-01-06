# import logging
import re
from scipy.stats import trim_mean
import pandas as pd


def convert_timestamp(timestamp_str):
    import pandas as pd

    # extract the timestamp
    timestamp = int(timestamp_str.strip("/Date()"))
    # convert to datetime
    datetime_obj = pd.to_datetime(timestamp, unit="ms")
    return datetime_obj


def convert_camel_to_snake(input_str: str) -> str:
    result = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", input_str).lower()
    return result


# clean up the financial ratios
def filter_financial_ratio(_df: pd.DataFrame) -> pd.DataFrame:
    _columns = [
        "quarter",
        "net_profit",
        "profit_growth_(%)",
        "revenue",
        "revenue_growth_(%)",
        "market_capital",
        "eps_(vnd)",
        "p/e",
        "outstanding_share",
        "roe_(%)",
        "symbol",
    ]

    _df = _df[_columns]

    _trimmed_mean_roe = trim_mean(_df["roe_(%)"].dropna(), 0.1)
    _trimmed_mean_market_capital = trim_mean(_df["market_capital"].dropna(), 0.1)
    _trimmed_mean_eps = trim_mean(_df["eps_(vnd)"].dropna(), 0.1)
    _trimmed_mean_pe = trim_mean(_df["p/e"].dropna(), 0.1)
    _trimmed_mean_outstanding_share = trim_mean(_df["outstanding_share"].dropna(), 0.1)

    _df["roe_(%)"].fillna(_trimmed_mean_roe, inplace=True)
    _df["market_capital"].fillna(_trimmed_mean_market_capital, inplace=True)
    _df["eps_(vnd)"].fillna(_trimmed_mean_eps, inplace=True)
    _df["p/e"].fillna(_trimmed_mean_pe, inplace=True)
    _df["outstanding_share"].fillna(_trimmed_mean_outstanding_share, inplace=True)
    # Add eps growth, profit growth, revenue growth
    _df["eps_growth(%)"] = (
        (_df["eps_(vnd)"] - _df.groupby("symbol")["eps_(vnd)"].shift(4))
        / _df.groupby("symbol")["eps_(vnd)"].shift(4)
    ) * 100
    _df["profit_growth_(%)"] *= 100
    _df["revenue_growth_(%)"] *= 100
    _df = _df.dropna()

    # _financial_ratios_cleaned = _df.dropna()
    return _df


# # clean up the daily price
# def process_dataframe(_df) -> pd.DataFrame:
#     _df["eps_growth(%)"] = (
#         (_df["eps_(vnd)"] - _df.groupby("symbol")["eps_(vnd)"].shift(4))
#         / _df.groupby("symbol")["eps_(vnd)"].shift(4)
#     ) * 100
#     _df = _df.dropna()

#     _df["profit_growth_(%)"] *= 100
#     _df["revenue_growth_(%)"] *= 100

#     _df_fundamental = _df[
#         [
#             "quarter",
#             "net_profit",
#             "profit_growth_(%)",
#             "revenue",
#             "revenue_growth_(%)",
#             "eps_(vnd)",
#             "eps_growth(%)",
#             "roe_(%)",
#             "symbol",
#         ]
#     ]
#     return _df_fundamental
