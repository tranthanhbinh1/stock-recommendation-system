import logging
from crawler.get_vn100 import get_vn100_symbols
import requests
from config.default import SSI_HEADERS
from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector
from datetime import datetime
from dataclasses import dataclass
import pandas as pd


@dataclass
class SSIHistoricalDailyPrice:
    DEFAULT_URL = "https://iboard.ssi.com.vn/dchart/api/history"

    @classmethod
    def get_historical_daily_price(
        cls,
        symbol: str,
        # from_date: str = datetime.today().strftime("%Y-%m-%d"),
        to_date: str = datetime.today().strftime("%Y-%m-%d"),
        URL: str = DEFAULT_URL,
    ):
        from_date = TimescaleConnector.get_last_call_date_hist_prices(symbol)
        from_timestamp = int(datetime.strptime(from_date, "%Y-%m-%d").timestamp())
        to_timestamp = int(datetime.strptime(to_date, "%Y-%m-%d").timestamp())

        df_list = []
        payload = {
            "symbol": symbol,
            "resolution": "d",
            "from": from_timestamp,
            "to": to_timestamp,
        }
        try:
            response = requests.get(
                url=URL,
                params=payload,
                headers=SSI_HEADERS,
            )
            logging.info(response.status_code)
            data = response.json()
            df_list.append(pd.DataFrame(data))
        except Exception as e:
            logging.error(repr(e))
        if not data:
            logging.info(f"No data for {symbol}")

        try:
            df_ = pd.concat(df_list)
            df_["symbol"] = symbol
        except ValueError as e:
            logging.error("No data!", repr(e))
            df_ = None

        if df_ is not None:
            df = pd.DataFrame()
            df = df.assign(
                symbol=df_["symbol"],
                date=pd.to_datetime(df_["t"], unit="s").dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                open=df_["o"],
                high=df_["h"],
                low=df_["l"],
                close=df_["c"],
                volume=df_["v"],
            )
            return df

        else:
            return None


if __name__ == "__main__":
    # set up logging to stdout
    setup_logging()
    crawler = SSIHistoricalDailyPrice()
    connector = TimescaleConnector()
    try:
        symbol_lst = TimescaleConnector.get_symbols()
    except Exception as e:
        logging.warning(repr(e))
        symbol_lst = get_vn100_symbols()
    logging.info(symbol_lst)
    for symbol in symbol_lst:
        logging.info(f"Getting data for {symbol}")
        try:
            df_ = crawler.get_historical_daily_price(symbol=symbol)
            TimescaleConnector.insert(
                df=df_, schema="market_data", table_name="ssi_daily_ohlcv"
            )
        except Exception as e:
            logging.error(repr(e))
    logging.info("Done!")
