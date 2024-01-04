import pandas as pd
from sqlalchemy import create_engine
from config.default import TS_DATABASE, TS_HOST, TS_PORT, TS_USERNAME, TS_PASSWORD
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimescaleConnector:
    conn_str = (
        f"postgresql://{TS_USERNAME}:{TS_PASSWORD}@{TS_HOST}:{TS_PORT}/{TS_DATABASE}"
    )
    connector = create_engine(conn_str)

    @classmethod
    def insert(
        cls, df: pd.DataFrame, schema: str, table_name: str, exist_strat: str = "append"
    ) -> None:
        df.to_sql(
            name=table_name,
            schema=schema,
            con=cls.conn_str,
            if_exists=exist_strat,
            index=False,
        )

    @classmethod
    def query_ohlcv_daily(cls, symbol) -> pd.DataFrame:
        query = f"""
        SELECT * FROM market_data.ssi_daily_ohlcv
        WHERE symbol = '{symbol}'
        """
        return pd.read_sql(
            query, cls.conn_str, index_col=["date"], parse_dates=["date"]
        )

    @classmethod
    def query_ohlcv_all(cls) -> pd.DataFrame:
        query = """
        SELECT * FROM market_data.ssi_daily_ohlcv
        """
        return pd.read_sql(query, cls.conn_str)

    @classmethod
    def query_financial_ratios(cls) -> pd.DataFrame:
        query = """
        SELECT * FROM financial_ratios.financial_ratios
        """
        return pd.read_sql(query, cls.conn_str)

    @classmethod
    def get_last_call_date_hist_prices(cls, symbol) -> pd.DataFrame:
        query = f"""
        SELECT MAX(date) FROM market_data.ssi_daily_ohlcv
        WHERE symbol = '{symbol}'
        """
        # return max + 1 day
        try:
            return (
                pd.read_sql(query, cls.conn_str).iloc[0, 0] + pd.Timedelta(days=1)
            ).strftime("%Y-%m-%d")
        except Exception:
            return "2017-01-01"
    
    @classmethod
    def get_latest_quarter_fin_ratios(cls) -> str:
        query = f"""
        SELECT MAX(ratio) 
        FROM financial_ratios.financial_ratios
        WHERE ratio LIKE '%%{str(datetime.now().year)}%%'   
        """
        return pd.read_sql(query, cls.conn_str)

    @classmethod
    def get_symbols(cls) -> pd.DataFrame:
        query = """
        SELECT DISTINCT symbol 
        FROM market_data.ssi_daily_ohlcv;
        """
        return pd.read_sql(query, cls.conn_str).symbol.to_list()
