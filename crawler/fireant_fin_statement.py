import requests
import pandas as pd
from dataclasses import dataclass
from crawler.get_vn100 import get_vn100_symbols
from config.default import FIREANT_HEADERS


@dataclass
class FireantFinStatement:
    DEFAULT_URL: str = "https://restv2.fireant.vn/symbols/{symbol}/full-financial-reports"
    # symbol_lst =  get_vn100_symbols()
    
    
    @classmethod
    def get_fireant_fin_statement(cls, symbol: str, type: int, year: int, quarter: int, limit: int = 25):
        payload = {
            "type": type,
            "year": year,
            "quarter": quarter,
            "limit": limit
        }

        url = cls.DEFAULT_URL.format(symbol=symbol)
        
        response = requests.get(url=url, params=payload, headers=FIREANT_HEADERS)
        data = response.json()
        
        df_ = pd.DataFrame(data, index=None)
        df_normalized = pd.json_normalize(df_["values"])

        
        return df_normalized