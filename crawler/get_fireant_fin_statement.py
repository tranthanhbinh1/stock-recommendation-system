import requests
import logging
import bson
from io import BytesIO
from dataclasses import dataclass
from crawler.get_vn100 import get_vn100_symbols
from config.default import FIREANT_HEADERS
from config.logging_config import setup_logging
from utils.mongo_connector import MongoConnector


@dataclass
class FireantFinStatement:
    DEFAULT_URL: str = (
        "https://restv2.fireant.vn/symbols/{symbol}/full-financial-reports"
    )
    # symbol_lst =  get_vn100_symbols()

    @classmethod
    def get_fireant_fin_statement(
        cls, symbol: str, type: int, year: int = 2023, quarter: int = 1, limit: int = 4
    ):
        payload = {"type": type, "year": year, "quarter": quarter, "limit": limit}
        url = cls.DEFAULT_URL.format(symbol=symbol)

        response = requests.get(url=url, params=payload, headers=FIREANT_HEADERS)
        data = BytesIO(response.content).getvalue()

        return data

    @classmethod
    def insert_to_mongo(cls, symbol: str, type: int, year: int = 2023, quarter: int = 1, limit: int = 4):
        _data = cls.get_fireant_fin_statement(symbol, type, year, quarter, limit)
        # print(_data)
        # print(type(_data))
        # Convert the data to a bson file so mongo can ingest
        _data = bson.BSON(_data).decode()
        
        try:
            MongoConnector.insert_to_mongo("balance_sheet", _data)
        except Exception as e:
            logging.error(repr(e))
    
