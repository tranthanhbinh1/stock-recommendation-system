import pandas as pd
import logging
import imgkit
from io import BytesIO  
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from .technical_analysis import TechnicalAnalysis
from utils.timescale_connector import TimescaleConnector
from config.logging_config import setup_logging

setup_logging()
logging.getLogger(__name__)


class MACrossover(Strategy):
    def init(self):
        self.ma5 = self.I(lambda x: x, self.data.MA5)
        self.ma20 = self.I(lambda x: x, self.data.MA20)

    def next(self):
        if not self.position and crossover(self.ma5, self.ma20):
            self.buy()
        elif self.position and crossover(self.ma20, self.ma5):
            self.position.close()


class Backtester(Backtest):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.technical = TechnicalAnalysis(
            df_technical=TimescaleConnector.query_ohlcv_daily(self.symbol)
        )
        self.data = (
            pd.DataFrame()
            .assign(
                Open=self.technical.df_technical.open,
                High=self.technical.df_technical.high,
                Low=self.technical.df_technical.low,
                Close=self.technical.df_technical.close,
                Volume=self.technical.df_technical.volume,
                MA5=self.technical.df_technical.MA5,
                MA20=self.technical.df_technical.MA20,
            )
            .astype(float)
            .set_index(self.technical.df_technical.index)
            .dropna()
        )

    def backtest(self):
        logging.info(self.data.info())
        bt = Backtest(self.data, MACrossover, cash=1000000000, commission=0.003)
        output = bt.run()
        plot = bt.plot()
        return output, plot


if __name__ == "__main__":
    backtester = Backtester(symbol="SSI")
    backtester.backtest()
