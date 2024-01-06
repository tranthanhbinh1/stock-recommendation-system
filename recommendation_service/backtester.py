# # Trading bot
import pandas as pd
import matplotlib.pyplot as plt
from utils.timescale_connector import TimescaleConnector



df = TimescaleConnector.query_ohlcv_all()
df["date"] = pd.to_datetime(df["date"])


df_tb = df.dropna()



df_tb.info()


df_tb.set_index("date", inplace=True)

def trading_strategy(df):
    buy_signals = []
    sell_signals = []

    for i in range(1, len(df)):
        if (
            df["MA5"].iloc[i] > df["MA20"].iloc[i]
            and df["MA5"].iloc[i - 1] < df["MA20"].iloc[i - 1]
        ):
            buy_signals.append(df.index[i])
        elif (
            df["MA5"].iloc[i] < df["MA20"].iloc[i]
            and df["MA5"].iloc[i - 1] > df["MA20"].iloc[i - 1]
        ):
            sell_signals.append(df.index[i])

    return buy_signals, sell_signals


buy_signals, sell_signals = trading_strategy(df_tb)


print("Buy Signals:")
for signal in buy_signals:
    print(signal)

print("\nSell Signals:")
for signal in sell_signals:
    print(signal)