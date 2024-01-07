import pandas as pd
import logging
from .technical_analysis import TechnicalAnalysis
from utils.timescale_connector import TimescaleConnector
from config.logging_config import setup_logging


setup_logging()
class Backtester:
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = TimescaleConnector.query_ohlcv_daily(symbol=self.symbol)
        self.buy_signals = []
        self.sell_signals = []

    def calculate_ma(self):
        analyzer = TechnicalAnalysis(df_technical=self.df)
        self.df = analyzer.calculate_ma()

    def trading_strategy(self):
        self.buy_signals = []
        self.sell_signals = []

        for i in range(1, len(self.df)):
            if (
                self.df["MA5"].iloc[i] > self.df["MA20"].iloc[i]
                and self.df["MA5"].iloc[i - 1] < self.df["MA20"].iloc[i - 1]
            ):
                self.buy_signals.append(self.df.index[i])
            elif (
                self.df["MA5"].iloc[i] < self.df["MA20"].iloc[i]
                and self.df["MA5"].iloc[i - 1] > self.df["MA20"].iloc[i - 1]
            ):
                self.sell_signals.append(self.df.index[i])

    def trading_signals(self):
        logging.info("Buy Signals:")
        buy_signals_df = pd.DataFrame(self.buy_signals, columns=["Signal"])
        logging.info(buy_signals_df)

        logging.info("\nSell Signals:")
        sell_signals_df = pd.DataFrame(self.sell_signals, columns=["Signal"])
        logging.info(sell_signals_df)

# Usage:
if __name__ == "__main__":
    backtester = Backtester(symbol="SSI")
    backtester.calculate_ma()
    backtester.trading_strategy()
    backtester.trading_signals()
