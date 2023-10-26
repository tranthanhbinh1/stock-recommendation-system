import logging
from crawler.get_vn100 import get_vn100_symbols
import requests
from config.default import SSI_HEADERS
from datetime import datetime
from dataclasses import dataclass
import pandas as pd


@dataclass
class SSIHistoricalDailyPrice:
    DEFAULT_URL = "https://iboard.ssi.com.vn/dchart/api/history"
    symbol_lst = get_vn100_symbols()

    @classmethod
    def get_historical_daily_price(cls, symbol: str, from_date: str, to_date: str, URL: str = DEFAULT_URL):
        from_timestamp = int(datetime.strptime(from_date, '%Y-%m-%d').timestamp())
        to_timestamp = int(datetime.strptime(to_date, '%Y-%m-%d').timestamp())

        payload = {
            "symbol": symbol,
            "resolution": "d",
            "from": from_timestamp,
            "to": to_timestamp,
        }
        response = requests.get(
            url=URL,
            params=payload,
            headers=SSI_HEADERS,
        )
        print(response.status_code)
        data = response.json()
        if not data:
            logging.info(f"No data for {symbol}")
            return None
        
        df_ = pd.DataFrame(data)
        
        return df_
