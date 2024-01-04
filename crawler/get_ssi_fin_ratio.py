from crawler.get_vn100 import get_vn100_symbols
from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector
from utils.utils import convert_camel_to_snake
from config.default import SSI_FIIN_HEADERS, SSI_DOWNLOAD_FIN_RATIO_URL
from dataclasses import dataclass
from io import BytesIO
import requests
import logging
import pandas as pd


@dataclass
class GetFinRatio:
    @classmethod
    def get_financial_ratios(
        cls,
        symbol: str = "VIC",
        timeline_from: str = "2016_4",
    ) -> pd.DataFrame:
        logging.info(f"Getting financial ratios of {symbol}")
        URL = SSI_DOWNLOAD_FIN_RATIO_URL.format(
            symbol=symbol, timeline_from=timeline_from
        )
        try:
            response = requests.get(
                url=URL,
                headers=SSI_FIIN_HEADERS,
            )
            buffer = BytesIO(response.content)
        except Exception as e:
            logging.error(repr(e))

        try:
            df_ = pd.read_excel(buffer)
            return df_
        except Exception as e:
            logging.error(repr(e))
            return pd.DataFrame()

    @staticmethod
    def fin_ratio_transformer(df_: pd.DataFrame, symbol: str) -> pd.DataFrame:
        # Reset and drop Indexes
        df_ = df_.iloc[6:]
        df_ = df_.iloc[:-4]  # Drop the "powered by fiintrade"
        df_ = df_.reset_index(drop=True)
        # Tranpose and reset the index again
        df_ = df_.transpose().reset_index(drop=True)
        # Set the first row as headers
        new_headers = df_.iloc[0]
        df_ = df_[1:]
        df_.columns = new_headers

        # Fill the columns with corresponding values
        df_.fillna(method="bfill", inplace=True, axis=1)

        # Remove the column that contains symbol names
        df_.drop(columns=symbol, inplace=True)

        # Convert column names from camelCase to snake_case
        df_.columns = df_.columns.map(convert_camel_to_snake)
        df_.columns = [col.replace(" ", "_") for col in df_.columns]

        # Assign a new column symbol
        df_ = df_.assign(symbol=symbol)
        # Rename ratio to quarter
        df_.rename(columns={"ratio": "quarter"}, inplace=True)

        return df_

    @staticmethod
    def insert_financial_ratios(df: pd.DataFrame) -> None:
        # Set the insert strat as "replace" for first time insertion, then "append"
        TimescaleConnector.insert(df, "market_data", "financial_ratios", "replace")


if __name__ == "__main__":
    setup_logging()
    symbol_lst = get_vn100_symbols()
    # Merge all dfs to create 1 big table
    merged_df = pd.DataFrame()
    for symbol in symbol_lst:
        df_ = GetFinRatio.get_financial_ratios(symbol)
        if df_.empty:
            continue
        df_ = GetFinRatio.fin_ratio_transformer(df_, symbol)
        # Logging out the df to check
        logging.info(df_.head())
        if merged_df.empty:
            merged_df = df_
            continue
        merged_df = pd.merge(merged_df, df_, how="outer")
        merged_df.to_csv("financial_ratios.csv")
    GetFinRatio.insert_financial_ratios(merged_df)
