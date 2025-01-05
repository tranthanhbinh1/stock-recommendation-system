import logging
import time
from dataclasses import dataclass
from typing import Literal

import requests

from config.default import FIREANT_HEADERS
from config.logging_config import setup_logging
from crawler.get_vn100 import get_vn100_symbols
from utils.mongo_connector import MongoConnector


@dataclass
class FireantFinStatement:
    DEFAULT_URL: str = (
        "https://restv2.fireant.vn/symbols/{symbol}/full-financial-reports"
    )
    # symbol_lst =  get_vn100_symbols()

    @classmethod
    def get_fireant_fin_statement(
        cls,
        symbol: str,
        type: Literal[1, 2, 3],
        year: int = 2023,
        quarter: int = 4,
        limit: int = 25,
    ):
        payload = {"type": type, "year": year, "quarter": quarter, "limit": limit}
        url = cls.DEFAULT_URL.format(symbol=symbol)

        response = requests.get(url=url, params=payload, headers=FIREANT_HEADERS)
        data = response.json()
        return data

    @classmethod
    def insert_to_mongo(cls, symbol: str, type: int):
        _data = cls.get_fireant_fin_statement(symbol, type)
        if not _data:
            logging.info(f"No data for {symbol}")
            return

        if type == 1:
            collection = "balance_sheet"
        elif type == 2:
            collection = "income_statement"
        elif type == 3:
            collection = "cash_flow"

        # Modify data to add 2 fields: Symbol and Type
        for item in _data:
            item["symbol"] = symbol
            item["type"] = type

        try:
            MongoConnector.insert_to_mongo(collection, _data)
            logging.info(
                f"Inserted data of symbol {symbol}, type {type} to {collection}"
            )
        except Exception as e:
            logging.error(repr(e))


if __name__ == "__main__":
    setup_logging()
    symbol_lst = get_vn100_symbols()
    for type in [1, 2, 3]:
        for symbol in symbol_lst:
            FireantFinStatement.insert_to_mongo(symbol, type)
            time.sleep(1)
