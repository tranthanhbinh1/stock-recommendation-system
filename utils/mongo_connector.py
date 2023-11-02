from dotenv import load_dotenv
import logging
import os
from pymongo import MongoClient
from dataclasses import dataclass
from config.default import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_AUTH_DB,
)


load_dotenv()


@dataclass
class MongoConnector:
    mongo_cli = MongoClient(
        host=MONGO_HOST,
        port=int(MONGO_PORT),
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        authSource=MONGO_AUTH_DB,
    )
    db = mongo_cli.financial_statements
    col_balance_sheet = db["balance_sheet"]
    col_income_statement = db["income_statement"]
    col_cash_flow = db["cash_flow"]
    
    @classmethod
    def insert_to_mongo(cls, collection, data):
        try:
            cls.db[collection].insert_one(data)
        except Exception as e:
            logging.error(repr(e))
    
    @classmethod
    def query_balance_sheet(symbol: str):
        pass
