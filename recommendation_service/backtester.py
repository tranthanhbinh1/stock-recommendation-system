import logging

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from config.logging_config import setup_logging
from utils.timescale_connector import PostgresConnector

from .technical_analysis import TechnicalAnalysis

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
    def __init__(self, symbol: str, nav: int = 10000000):
        self.symbol = symbol
        self.nav = nav
        self.technical = TechnicalAnalysis(
            df_technical=PostgresConnector.query_ohlcv_daily(self.symbol)
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

    def get_backtest_plot(self):
        bt = Backtest(self.data, MACrossover, cash=self.nav, commission=0.003)
        bt.run()
        plot = bt.plot()
        # imgkit.from_file("MACrossover.html", "out.png")
        return plot

    def get_backtest_sells_buys(self):
        output = Backtest(self.data, MACrossover, cash=self.nav, commission=0.003).run()
        trades = pd.DataFrame(output.get("_trades"))
        # Change duration, entry and exit time to string
        trades["Duration"] = trades["Duration"].astype(str)
        trades["EntryTime"] = trades["EntryTime"].astype(str)
        trades["ExitTime"] = trades["ExitTime"].astype(str)
        trades = trades.to_dict(orient="records")
        return trades

    def get_backtest_summary(self):
        output = Backtest(self.data, MACrossover, cash=self.nav, commission=0.003).run()

        output.head(27).to_csv("backtest.csv")
        output = output.head(27)
        # Convert all to strings first
        output = output.astype(str)
        return output.to_dict()


if __name__ == "__main__":
    backtester = Backtester(symbol="SSI")
    rec = backtester.get_backtest_summary()
