import warnings
from dataclasses import dataclass

import pandas as pd

from config.logging_config import setup_logging

warnings.filterwarnings("ignore")
setup_logging()


@dataclass
class TechnicalAnalysis:
    df_technical: pd.DataFrame

    def __post_init__(self):
        self.calculate_ema()
        self.calculate_ma()

    # fmt: off
    # Start of Technical Rules
    # Calculate EMA34-89 for each stock
    def calculate_ema(self) -> pd.DataFrame:
        for i in [34, 89]:
            self.df_technical[f"EMA{i}"] = (
                self.df_technical
                .groupby("symbol")["close"]
                .transform(lambda x: x.ewm(span=i, adjust=False).mean())
                .dropna()
            )
        return self.df_technical

    # Calculate MACD for each stock
    def calculate_ma(self) -> pd.DataFrame:
        for i in [5, 10, 20, 50, 150, 200]:
            self.df_technical[f"MA{i}"] = (
                self.df_technical\
                .groupby("symbol")["close"]
                .transform(lambda x: x.rolling(i).mean())
                .dropna()
            )
        return self.df_technical    
    
    def check_emacross_8thcondition(self) -> pd.DataFrame:
        self.df_technical["EMA_Condition_Met"] = self.df_technical["EMA34"] > self.df_technical["EMA89"]
        result = self.df_technical.groupby("symbol")["EMA_Condition_Met"].any()
        result.symbol = result.index
        return result
    
    def check_ma_9thcondition(self) -> pd.DataFrame:
        self.df_technical["MA_Condition_Met"] = (
            self.df_technical["MA50"] > self.df_technical["MA150"]
        ) & (self.df_technical["MA150"] > self.df_technical["MA200"])
        result = self.df_technical.groupby("symbol")["MA_Condition_Met"].any()
        result.symbol = result.index
        return result
