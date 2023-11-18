from crawler.get_vn100 import get_vn100_symbols
from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector
from utils.utils import convert_camel_to_snake
from config.default import SSI_FIIN_HEADERS, SSI_DOWNLOAD_FIN_RATIO_URL
from dataclasses import dataclass
from io import BytesIO
import requests
import logging
import time
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
    def fin_ratio_transformer(df_: pd.DataFrame, symbol: str):
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
        cols = pd.Series(df_.columns)
        # Remove the duplicated symbol columns
        for dup in cols[cols.duplicated()].unique():
            cols[cols[cols == dup].index.values.tolist()] = [
                dup + "_" + str(i) if i != 0 else dup for i in range(sum(cols == dup))
            ]
        df_.columns = cols

        # fmt: off
        symbols_columns = df_.columns[df_.columns.astype(str).str.contains(symbol)].tolist()
        valid_columns = df_.columns[~df_.columns.astype(str).str.contains(symbol)].to_list()
        valid_columns_final = [col for col in valid_columns if col not in ["Ratio", "Profit Growth (%)", "Revenue Growth (%)"]]

        # fmt: on
        # Name mapping from tickers to valid names
        name_mapping = dict(zip(symbols_columns, valid_columns_final))

        # Remove the empty columns first
        df_ = df_.drop(columns=valid_columns)
        df_.assign(symbol=symbol)

        # Rename
        df_.rename(columns=name_mapping, inplace=True)

        return df_

    @staticmethod
    def insert_financial_ratios(df: pd.DataFrame) -> None:
        df.columns = [convert_camel_to_snake(str(col)) for col in df.columns]

        TimescaleConnector.insert(df, "market_data", "financial_ratios")


if __name__ == "__main__":
    setup_logging()
    symbol_lst = get_vn100_symbols()
    for symbol in symbol_lst:
        df_ = GetFinRatio.get_financial_ratios(symbol)
        if df_.empty:
            continue
        df_ = GetFinRatio.fin_ratio_transformer(df_, symbol)
        # GetFinRatio.insert_financial_ratios(df_)
        time.sleep(0.5)

#TODO: not usable yet