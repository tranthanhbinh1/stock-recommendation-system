import requests
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from config.default import FIREANT_HEADERS
from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector
import pandas as pd


@dataclass
class FireantHistoricalVnIndex:
    DEFAULT_URL: str = "https://restv2.fireant.vn/symbols/VNINDEX/historical-quotes"

    @classmethod
    def get_fireant_historical_vnindex(cls) -> pd.DataFrame:
        payload = {
            "startDate": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            "endDate": datetime.now().strftime("%Y-%m-%d"),
            "limit": 1000,
        }
        try:
            response = requests.get(
                url=cls.DEFAULT_URL, params=payload, headers=FIREANT_HEADERS
            )
            data = response.json()
            df = pd.DataFrame(data)
        except Exception as e:
            logging.error(repr(e))
            exit

        return df

    @classmethod
    def transform_data(cls) -> pd.DataFrame:
        df_ = FireantHistoricalVnIndex.get_fireant_historical_vnindex()
        df = pd.DataFrame().assign(
            date=df_.date,
            open=df_.priceOpen,
            high=df_.priceHigh,
            low=df_.priceLow,
            close=df_.priceClose,
            volume=df_.totalVolume,
        )
        # reverse the order of the df
        df = df[::-1]
        # Shift this up 1 row
        df["percent_change"] = (df["close"] - df["close"].shift(1)) / df["close"] * 100

if __name__ == "__main__":
    setup_logging()
    df = FireantHistoricalVnIndex.transform_data()
    TimescaleConnector.insert(
        df=df,
        table_name="historical_vnindex",
        schema="market_data",
        exist_strat="replace",
    )
