import pandas as pd
from sqlalchemy import create_engine
from config.default import TS_DATABASE, TS_HOST, TS_USERNAME, TS_PASSWORD
from dataclasses import dataclass


@dataclass
class TimescaleConnector():
    connector = create_engine(
        f"postgresql://{TS_USERNAME}:{TS_PASSWORD}@{TS_HOST}:5432/{TS_DATABASE}"
    )
    
    @classmethod
    def query_ohlcv_daily():
        pass