import logging
from functools import lru_cache

import pandas as pd

from config.logging_config import setup_logging
from utils.postgres_connector import PostgresConnector

setup_logging()


class SectorRanking:
    def __init__(self):
        self.industries = None
        self.prices_1y = None
        self.vnindex_1y = None
        self.ranked_sectors = None

    @lru_cache(maxsize=1)
    def load_data(self):
        logging.info("Loading data...")
        self.industries = PostgresConnector.query_by_sql(
            """
            SELECT * FROM market_data.industries_sectors
            """
        )

        self.prices_1y = PostgresConnector.query_ohlcv_1y_interval()
        self.prices_1y = self.prices_1y.merge(
            self.industries, on="symbol", how="left"
        ).astype({"close": float})
        self.prices_1y["stock_price_change"] = self.prices_1y.groupby(
            "symbol"
        ).close.pct_change()
        self.vnindex_1y = PostgresConnector.query_vnindex_1y_interval()
        self.vnindex_1y.dropna()
        self.prices_1y.dropna()

        self.vnindex_1y.date = pd.to_datetime(self.vnindex_1y.date)
        self.prices_1y.date = pd.to_datetime(self.prices_1y.date)

    @lru_cache(maxsize=1)
    def calculate_ranking(self):
        logging.info("Calculating ranking...")
        prices_merged = self.prices_1y.merge(
            self.vnindex_1y[["date", "percent_change"]], on="date", how="left"
        ).dropna()
        grouped = prices_merged.groupby("industry_sector").agg(
            {"stock_price_change": "mean", "percent_change": "mean"}
        )
        grouped["RS"] = grouped["stock_price_change"] / grouped["percent_change"]
        self.ranked_sectors = grouped.sort_values(by="RS", ascending=False)
        self.ranked_sectors.reset_index(inplace=True)
        self.ranked_sectors["ranking"] = (
            self.ranked_sectors.reset_index(drop=False).index + 1
        )
        logging.info(self.ranked_sectors)
        return self.ranked_sectors


if __name__ == "__main__":
    sector_ranking = SectorRanking()
    sector_ranking.load_data()
    sector_ranking.calculate_ranking()
