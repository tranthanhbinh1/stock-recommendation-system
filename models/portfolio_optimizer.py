
from scipy.optimize import minimize
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import trim_mean


# DEFAULT
top_stocks = 

# Modern Porfolio Theory
df_porfolio_3stocks_highrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_3stocks_highrisk.head()

df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.drop(
    [
        "SJS",
        "HCM",
        "VGC",
        "VNM",
        "CTD",
        "NKG",
        "MWG",
    ],
    axis=1,
)

df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.dropna()
df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.reset_index()
df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.drop(["index"], axis=1)
df_porfolio_3stocks_highrisk["date"] = pd.to_datetime(
    df_porfolio_3stocks_highrisk["date"]
)

# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_3stocks_highrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()

# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252


# Calculate the porfolio standard deviation
def standard_deviation(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)


# Calculate the expected return
def expected_return(weights, log_returns):
    return np.sum(log_returns.mean() * weights) * 252


# Calculate the sharpe ratio
def sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    return (expected_return(weights, log_returns) - risk_free_rate) / standard_deviation(
        weights, cov_matrix
    )


# Set the risk free rate
risk_free_rate = 0.02


def neg_sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_3stocks_highrisk.columns.drop("date")


# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")

# #### Portfolio of 3 stocks with mediuma and low risk


df_porfolio_3stocks_mediumrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)

df_porfolio_3stocks_mediumrisk = 

df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.dropna()
df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.reset_index()
df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.drop(["index"], axis=1)
df_porfolio_3stocks_mediumrisk["date"] = pd.to_datetime(
    df_porfolio_3stocks_mediumrisk["date"]
)

# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_3stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()


tickers = df_porfolio_3stocks_mediumrisk.columns.drop("date")

# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.35) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 3 stocks with low risk
# #### Portfolio of 5 stocks with high risk


df_porfolio_optimization = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_optimization.head()


df_porfolio_optimization.isnull().sum()


df_porfolio_optimization = df_porfolio_optimization.drop(
    ["SJS", "HCM", "VGC", "VNM", "CTD"], axis=1
)


df_porfolio_optimization = df_porfolio_optimization.dropna()


df_porfolio_optimization = df_porfolio_optimization.reset_index()


df_porfolio_optimization = df_porfolio_optimization.drop(["index"], axis=1)


df_porfolio_optimization["date"] = pd.to_datetime(df_porfolio_optimization["date"])


df_porfolio_optimization.dtypes


df_porfolio_optimization.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_optimization.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


log_returns.isnull().sum()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252


tickers = df_porfolio_optimization.columns.drop("date")


# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]


# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
initial_weights


# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)


# Get optimal weights
optimal_weights = optimized_results.x


print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")



num_portfolios = 10000
all_weights = np.zeros((num_portfolios, len(tickers)))
ret_arr = np.zeros(num_portfolios)
vol_arr = np.zeros(num_portfolios)
sharpe_arr = np.zeros(num_portfolios)

for i in range(num_portfolios):
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)

    all_weights[i, :] = weights
    ret_arr[i] = expected_return(weights, log_returns)
    vol_arr[i] = standard_deviation(weights, cov_matrix)
    sharpe_arr[i] = sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)
max_sharpe_idx = sharpe_arr.argmax()
max_sharpe_return = ret_arr[max_sharpe_idx]
max_sharpe_volatility = vol_arr[max_sharpe_idx]

# #### Portfolio of 5 stocks with medium risk


df_porfolio_5stocks_mediumrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_5stocks_mediumrisk.head()


df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.drop(
    ["SJS", "HCM", "VGC", "VNM", "CTD"], axis=1
)


df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.dropna()
df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.reset_index()
df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.drop(["index"], axis=1)
df_porfolio_5stocks_mediumrisk["date"] = pd.to_datetime(
    df_porfolio_5stocks_mediumrisk["date"]
)


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_5stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252

tickers = df_porfolio_5stocks_mediumrisk.columns.drop("date")


# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.35) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 5 stocks with low risk


df_porfolio_5stocks_lowrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_5stocks_lowrisk.head()


df_porfolio_5stocks_lowrisk.isnull().sum()


df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.drop(
    ["SJS", "HCM", "VGC", "VNM", "CTD"], axis=1
)


df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.dropna()
df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.reset_index()
df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.drop(["index"], axis=1)
df_porfolio_5stocks_lowrisk["date"] = pd.to_datetime(
    df_porfolio_5stocks_lowrisk["date"]
)


df_porfolio_5stocks_lowrisk.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_5stocks_lowrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252

tickers = df_porfolio_5stocks_lowrisk.columns.drop("date")


# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.25) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with high risk


df_porfolio_10stocks_highrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_10stocks_highrisk.head()


df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.dropna()
df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.reset_index()
df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.drop(["index"], axis=1)
df_porfolio_10stocks_highrisk["date"] = pd.to_datetime(
    df_porfolio_10stocks_highrisk["date"]
)


df_porfolio_10stocks_highrisk.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_highrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252


tickers = df_porfolio_10stocks_highrisk.columns.drop("date")


# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with medium risk


df_porfolio_10stocks_mediumrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_10stocks_mediumrisk.head()


df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.dropna()
df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.reset_index()
df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.drop(
    ["index"], axis=1
)
df_porfolio_10stocks_mediumrisk["date"] = pd.to_datetime(
    df_porfolio_10stocks_mediumrisk["date"]
)


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()

# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov() * 252

tickers = df_porfolio_10stocks_mediumrisk.columns.drop("date")

# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.3) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with low risk


df_porfolio_10stocks_lowrisk = pd.read_csv(
    "C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv"
)
df_porfolio_10stocks_lowrisk.head()


df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.dropna()
df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.reset_index()
df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.drop(["index"], axis=1)
df_porfolio_10stocks_lowrisk["date"] = pd.to_datetime(
    df_porfolio_10stocks_lowrisk["date"]
)


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_lowrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()

tickers = df_porfolio_10stocks_lowrisk.columns.drop("date")

# Set the constraints and bounds
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.2) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(
    neg_sharpe_ratio,
    initial_weights,
    args=(log_returns, cov_matrix, risk_free_rate),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds,
)
# Get optimal weights
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(
    optimal_weights, log_returns, cov_matrix, risk_free_rate
)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# The formula to calculate the annual return of a portfolio based on the buy/sell signals from the trading bot, combined with the weighting of each stock according to Modern Portfolio Theory:
#
# #### Portfolio Annual Return = (ReturnSSI x WeightSSI) + (ReturnVND x WeightVND) + (ReturnHPG x WeightHPG)


# Annual returns of each stock
annual_return_ssi = 35.90
annual_return_vnd = 69.57
annual_return_hpg = 26.92
# Weights of each stock in the portfolio
weight_ssi = 0.2310
weight_vnd = 0.4000
weight_hpg = 0.3690
# Calculating the weighted average of the portfolio's annual return
portfolio_annual_return = (
    (annual_return_ssi * weight_ssi)
    + (annual_return_vnd * weight_vnd)
    + (annual_return_hpg * weight_hpg)
)