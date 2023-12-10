
# # Data preparation


import warnings
# Ignoring future warnings and deprecation warnings so as not to make the notebook full of warnings
warnings.filterwarnings("ignore")


import pandas as pd
df = pd.read_csv('C:/Users/admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/financial_ratios.csv')
df.head()


df.shape


df.info()


null_counts = df.isnull().sum()
null_counts


df = df.drop(['net_interest_income_growth_(%)', 
              'net_interest_income', 
              'fixed_asset_turnover', 
              'interest_coverage', 
              'financial_leverage',
              '(st_+_lt_borrowings)/equity',
              'asset_turnover',
              'current_ratio',
              'ebit_margin_(%)',
              'days_payable_outstanding',
              'quick_ratio',
              'days_inventory_outstanding',
              'days_sales_outstanding',
              'roa_(%)',
              'dept/equity',
              'cash_ratio',
              'bvps_(vnd)',
              'ev/ebitda',
              'p/cash_flow',
              'p/s',
              'p/b',
              'cash_cycle',
              'Unnamed: 0'
             ], axis=1)


df = df.drop(['roic_(%)',
              'net_profit_margin_(%)',
              'gross_profit_margin_(%)',
             ], axis=1)


df.head()


rows_with_null_roe = df[df['roe_(%)'].isnull()]

rows_with_null_roe.head()


from scipy.stats import trim_mean
trimmed_mean_roe = trim_mean(df['roe_(%)'].dropna(), 0.1)

df['roe_(%)'].fillna(trimmed_mean_roe, inplace=True)


trimmed_mean_market_capital = trim_mean(df['market_capital'].dropna(), 0.1)
trimmed_mean_eps = trim_mean(df['eps_(vnd)'].dropna(), 0.1)
trimmed_mean_pe = trim_mean(df['p/e'].dropna(), 0.1)
trimmed_mean_outstanding_share = trim_mean(df['outstanding_share'].dropna(), 0.1)

df['market_capital'].fillna(trimmed_mean_market_capital, inplace=True)
df['eps_(vnd)'].fillna(trimmed_mean_eps, inplace=True)
df['p/e'].fillna(trimmed_mean_pe, inplace=True)
df['outstanding_share'].fillna(trimmed_mean_outstanding_share, inplace=True)


revenue_null_value = df[df['revenue'].isnull()]
revenue_null_value.head(5)


df = df.dropna()


null_counts = df.isnull().sum()
null_counts


df.head()


df.info()


df.to_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/financial_ratios_cleaned.csv')


# # Rule-based for medium and long-term trading


# ### Industry sector analysis


# The Relative Strength (RS) indicator, often used in stock analysis, is a measure of a stock's or a sector's performance relative to a broader market index or another benchmark. The RS calculation is typically based on the ratio of the average returns (or price changes) of the stock or sector to the average returns of the market index over the same period.


# 1. Determine the Period of Analysis: 5/9/2022 - 31/8/2023


# 2. Calculate the Percentage Change: For each period in your chosen time frame, calculate the percentage change in price for both the stock (or sector) and the market index. The formula for percentage change is:
# #### Percentage Change = [(Current Price − Previous Price)/Previous Price] ×100


# 3. Compute the Average Percentage Change: Calculate the average of these percentage changes over the entire period for both the stock (or sector) and the index.


# 4. Calculate RS: Divide the average percentage change of the stock (or sector) by the average percentage change of the market index. The formula is:
# 
# #### RS =  Average Percentage Change of Industry Sector / Average Percentage Change of Market Index
# ​
#  
# 


import pandas as pd
df_VNINDEX = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/Dữ liệu Lịch sử VN Index.csv')
df_VNINDEX.head()


df_VNINDEX['Ngày'] = pd.to_datetime(df_VNINDEX['Ngày'])


df_sorted = df_VNINDEX.sort_values(by='Ngày')
df_sorted


df_sorted.to_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/Dữ liệu Lịch sử VN Index.csv')


df_industry_sector = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/Industry_sector_analysis.csv', encoding='ISO-8859-1')
df_industry_sector.head()


df_industry_sector = df_industry_sector.dropna()


df_industry_sector.isnull().sum()


unique_value = df_industry_sector['industry sector'].unique()
unique_value


corrections = {
    'Hóa Ch?t': 'Hóa Chất',
    'Hóa ch?t': 'Hóa Chất',
    'B?t ??ng s?n': 'Bất Động Sản',
    'S?n xu?t th?c ph?m': 'Sản xuất thực phẩm',
    'D?ch v? tài chính': 'Dịch vụ tài chính',
    'Xây d?ng và v?t li?u': 'Xây dựng và vật liệu',
    'B?o hi?m nhân th?': 'Bảo hiểm nhân thọ',
    'N??c và khí ??t': 'Nước và khí đốt',
    'Ph?n m?m d?ch v? máy tính': 'Phần mềm dịch vụ máy tính',
    'Bán l?': 'Bán lẻ',
    'Lâm nghi?p và gi?y': 'Lâm nghiệp và giấy',
    'Ph?n m?m và d?ch v? máy tính': 'Phần mềm và dịch vụ máy tính',
    'S?n xu?t và phân ph?i ?i?n': 'Sản xuất và phân phối điện',
    '?i?n t? và thi?t b? ?i?n': 'Điện tử và thiết bị điện',
    'V?n t?i': 'Vận tải',
    'Kim lo?i': 'Kim loại',
    'D??c ph?m': 'Dược phẩm',
    'S?n xu?t d??c ph?m': 'Sản xuất dược phẩm',
    'S?n xu?t d?u khí': 'Sản xuất dầu khí',
    'Hàng cá nhân': 'Hàng cá nhân',
    'Thi?t b?, d?ch v? và phân ph?i d?u khí': 'Thiết bị, dịch vụ và phân phối dầu khí',
    'Công nghi?p n?ng': 'Công nghiệp nặng',
    'Bia và ?? u?ng': 'Bia và đồ uống',
    'Thi?t b? và ph?n c?ng': 'Thiết bị và phần cứng',
    'Du l?ch và gi?i trí': 'Du lịch và giải trí',
    'Ch? s? th? tr??ng chung': 'Chỉ số thị trường chung'
}

# Replace the values
df_industry_sector['industry sector'] = df_industry_sector['industry sector'].replace(corrections)


df_industry_sector = df_industry_sector.reset_index()


df_industry_sector = df_industry_sector.drop(['index'], axis=1)


df_industry_sector


# Convert 'date' to datetime format
df_industry_sector['date'] = pd.to_datetime(df_industry_sector['date'])

# Convert 'close' to numeric, handling non-numeric values
# 'coerce' will set invalid parsing to NaN
df_industry_sector['close'] = pd.to_numeric(df_industry_sector['close'], errors='coerce')

# Drop rows where 'close' is NaN after conversion (if any)
df_industry_sector.dropna(subset=['close'], inplace=True)

# Separate VN-Index data
df_vn_index = df_industry_sector[df_industry_sector['symbol'] == 'VN-Index']

# Calculate percentage change for VN-Index
df_vn_index['vn_index_change'] = df_vn_index['close'].pct_change()

# Calculate percentage change for each stock
df_industry_sector['stock_price_change'] = df_industry_sector.groupby('symbol')['close'].pct_change()

# Merge VN-Index changes back into the main DataFrame
df_merged = df_industry_sector.merge(df_vn_index[['date', 'vn_index_change']], on='date', how='left')

# Group by industry sector and calculate the average of stock and VN-Index changes
grouped = df_merged.groupby('industry sector').agg({'stock_price_change': 'mean', 'vn_index_change': 'mean'})

# Calculate Relative Strength (RS)
grouped['RS'] = grouped['stock_price_change'] / grouped['vn_index_change']

# The 'RS' column now contains the Relative Strength of each industry sector
grouped['RS']


# Sort the sectors based on RS in descending order
ranked_sectors = grouped.sort_values(by='RS', ascending=False)

# Reset the index to make 'industry sector' a column again, if it's the index
ranked_sectors.reset_index(inplace=True)

# Add a ranking column that starts from 1
ranked_sectors['Ranking'] = ranked_sectors.reset_index(drop=False).index + 1

ranked_sectors


# ### Fundamental Analysis Conditions


df['eps_growth(%)'] = ((df['eps_(vnd)'] - df.groupby('symbol')['eps_(vnd)'].shift(4)) / df.groupby('symbol')['eps_(vnd)'].shift(4)) * 100


df.isnull().sum()


df = df.dropna()


df['profit_growth_(%)'] *= 100
df['revenue_growth_(%)'] *= 100


df.head(5)


df.to_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/financial_ratios_cleaned.csv')


df_fundamental = df[['ratio','net_profit', 'profit_growth_(%)', 'revenue', 'revenue_growth_(%)','eps_(vnd)', 'eps_growth(%)', 'roe_(%)', 'symbol']]
df_fundamental


# The most recent quarter's EPS growth is greater than 15% compared to the same quarter of the previous year
def check_eps_growth_1stcondition(df_fundamental, latest_quarter, growth_threshold):
    # Filter DataFrame for the latest quarter
    latest_quarter_df = df_fundamental[df_fundamental['ratio'] == latest_quarter]
    # Check if the EPS growth is greater than the specified threshold
    latest_quarter_df['condition_met'] = latest_quarter_df['eps_growth(%)'] > growth_threshold
    return latest_quarter_df[['symbol', 'eps_growth(%)', 'condition_met']]

result_1st = check_eps_growth_1stcondition(df_fundamental, 'Q3 2023', 15)

result_1st.head()


# EPS growth for the two most recent quarters is greater than 15% compared to the same quarters of the previous year
def check_eps_growth_2ndcondition(df_fundamental, recent_quarters, growth_threshold):
    # Filter DataFrame for the recent quarters
    recent_quarter_df = df_fundamental[df_fundamental['ratio'].isin(recent_quarters)]

    # Group by stock symbol and check if EPS growth is greater than the threshold for all recent quarters
    result = recent_quarter_df.groupby('symbol').apply(
        lambda x: (x['eps_growth(%)'] > growth_threshold).all()
    )

    return result

recent_2nd = ['Q3 2023', 'Q2 2023']
result_2nd = check_eps_growth_2ndcondition(df_fundamental, recent_quarters, 15)

result_2nd.head()


# Earnings Per Share (EPS) in each quarter of the last 12 months is at or near its peak
def assess_eps_near_peak_3rdcondition(df_fundamental, year):
    # Filter DataFrame for the specified year
    year_df = df_fundamental[df_fundamental['ratio'].str.contains(year)]

    # Function to check if EPS is at or near peak for each stock
    def is_eps_at_peak(stock_df):
        # Track the maximum EPS value encountered
        max_eps = 0
        for eps in stock_df['eps_(vnd)']:
            # Define "near peak" criteria (e.g., within 5% of the max)
            near_peak = max_eps * 0.95
            if eps < near_peak:
                return False
            max_eps = max(max_eps, eps)
        return True

    # Group by stock symbol and apply the check
    result = year_df.groupby('symbol').apply(is_eps_at_peak)
    
    return result

result_3rd = assess_eps_near_peak_3rdcondition(df, '2023')

result_3rd.head()


# Most recent quarter's revenue is greater than 20% compared to the same quarter of the previous year
def check_revenue_growth_4thcondition(df_fundamental, latest_quarter, growth_threshold):
    # Filter DataFrame for the latest quarter
    latest_quarter_df = df_fundamental[df_fundamental['ratio'] == latest_quarter]

    # Check if the revenue growth is greater than the specified threshold
    latest_quarter_df['condition_met'] = latest_quarter_df['revenue_growth_(%)'] > growth_threshold

    # Return the DataFrame with an additional column indicating if the condition is met
    return latest_quarter_df[['symbol', 'revenue_growth_(%)', 'condition_met']]

result_4th = check_revenue_growth_4thcondition(df_fundamental, 'Q3 2023', 20)

result_4th.head()


# Accelerating revenue growth over the last three quarters
def check_accelerating_revenue_growth_5thcondition(df_fundamental, quarters):
    # Filter DataFrame for the specified quarters
    filtered_df = df_fundamental[df_fundamental['ratio'].isin(quarters)]

    # Function to check if revenue growth is accelerating for each stock
    def is_growth_accelerating(stock_df):
        # Ensure the DataFrame is sorted by quarter
        stock_df = stock_df.sort_values(by='ratio')
        growth_rates = stock_df['revenue_growth_(%)'].tolist()

        # Check if each subsequent growth rate is greater than the previous
        return all(x < y for x, y in zip(growth_rates, growth_rates[1:]))

    # Group by stock symbol and apply the check
    result = filtered_df.groupby('symbol').apply(is_growth_accelerating)

    return result

relevant_quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023']
result_5th = check_accelerating_revenue_growth_5thcondition(df_fundamental, relevant_quarters)

result_5th.head()


# Accelerating profit growth over the last three quarters
def check_accelerating_profit_growth_6thcondition(df_fundamental, quarters):
    # Filter DataFrame for the specified quarters
    filtered_df = df_fundamental[df_fundamental['ratio'].isin(quarters)]

    # Function to check if revenue growth is accelerating for each stock
    def is_growth_accelerating(stock_df):
        # Ensure the DataFrame is sorted by quarter
        stock_df = stock_df.sort_values(by='ratio')
        growth_rates = stock_df['profit_growth_(%)'].tolist()

        # Check if each subsequent growth rate is greater than the previous
        return all(x < y for x, y in zip(growth_rates, growth_rates[1:]))

    # Group by stock symbol and apply the check
    result = filtered_df.groupby('symbol').apply(is_growth_accelerating)

    return result

relevant_quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023']
result_6th = check_accelerating_profit_growth_6thcondition(df_fundamental, relevant_quarters)

result_6th.head()


def check_roe_7thcondition(df_fundamental, current_quarter, roe_threshold):
    # Filter DataFrame for the current quarter
    current_quarter_df = df_fundamental[df_fundamental['ratio'] == current_quarter]

    # Check if the ROE is at least the specified threshold
    current_quarter_df['condition_met'] = current_quarter_df['roe_(%)'] >= roe_threshold

    # Return the DataFrame with an additional column indicating if the condition is met
    return current_quarter_df[['symbol', 'roe_(%)', 'condition_met']]

result_7th = check_roe_7thcondition(df_fundamental, 'Q3 2023', 15)

result_7th.head()


# ### Technical Analysis Conditions


df_technical = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/stock_price.csv')
df_technical.head()


df_technical['date'] = pd.to_datetime(df_technical['date'])


df_technical.dtypes


# Calculate EMA34-89 for each stock
df_technical['EMA34'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.ewm(span=34, adjust=False).mean())
df_technical['EMA89'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.ewm(span=89, adjust=False).mean())
df_technical.head()


# Calculate MA5-20-50-150-200 for each stock
df_technical['MA5'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.rolling(window=5).mean())
df_technical['MA20'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.rolling(window=20).mean())
df_technical['MA50'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.rolling(window=50).mean())
df_technical['MA150'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.rolling(window=150).mean())
df_technical['MA200'] = df_technical.groupby('symbol')['close'].transform(lambda x: x.rolling(window=200).mean())
df_technical.head()


df_technical = df_technical.dropna()
df_technical.head()


df_technical.shape


df_technical = df_technical.reset_index()


df_technical = df_technical.drop(['index'], axis=1)


df_technical


def check_emacross_8thcondition(df_technical):
    df_technical['EMA_Condition_Met'] = df_technical['EMA34'] > df_technical['EMA89']
    condition_met_by_stock = df_technical.groupby('symbol')['EMA_Condition_Met'].any()

    return condition_met_by_stock
result_8th = check_emacross_8thcondition(df_technical)
result_8th.head()


def check_ma_9thcondition(df_technical):
    df_technical['MA_Condition_Met'] = (df_technical['MA50'] > df_technical['MA150']) & (df_technical['MA150'] > df_technical['MA200'])
    condition_met_by_stock = df_technical.groupby('symbol')['MA_Condition_Met'].any()
    return condition_met_by_stock
result_9th = check_ma_9thcondition(df_technical)
result_9th.head()


df_technical.to_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/stock_price_cleaned.csv')


# ### Conditions Evaluation


def evaluate_and_rank_stocks(df_fundamental, df_technical):
    latest_quarter = 'Q3 2023'
    recent_two_quarters = ['Q3 2023', 'Q2 2023']
    recent_three_quarters = ['Q3 2023', 'Q2 2023', 'Q1 2023']
    year = '2023'

    condition_1 = check_eps_growth_1stcondition(df_fundamental, latest_quarter, 15)['condition_met']
    condition_2 = check_eps_growth_2ndcondition(df_fundamental, recent_two_quarters, 15)
    condition_3 = assess_eps_near_peak_3rdcondition(df_fundamental, year)
    condition_4 = check_revenue_growth_4thcondition(df_fundamental, latest_quarter, 20)['condition_met']
    condition_5 = check_accelerating_revenue_growth_5thcondition(df_fundamental, recent_three_quarters)
    condition_6 = check_accelerating_profit_growth_6thcondition(df_fundamental, recent_three_quarters)
    condition_7 = check_roe_7thcondition(df_fundamental, latest_quarter, 15)['condition_met']
    condition_8 = check_emacross_8thcondition(df_technical)
    condition_9 = check_ma_9thcondition(df_technical)

    combined = pd.DataFrame({
        'Condition 1': condition_1,
        'Condition 2': condition_2,
        'Condition 3': condition_3,
        'Condition 4': condition_4,
        'Condition 5': condition_5,
        'Condition 6': condition_6,
        'Condition 7': condition_7,
        'Condition 8': condition_8,
        'Condition 9': condition_9
    })

    combined['Total Conditions Met'] = combined.sum(axis=1)

    ranked_stocks = combined.sort_values(by='Total Conditions Met', ascending=False)

    return ranked_stocks

ranked_stocks = evaluate_and_rank_stocks(df_fundamental, df_technical)


ranked_stocks['Ranking'] = ranked_stocks['Total Conditions Met'].rank(ascending=False, method='first').astype(int)
ranked_stocks.head(10)


ranked_stocks.to_excel('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/stock_ranking.xlsx', index=False)


# # Trading bot 
# 


# ### 1. SSI


import pandas as pd
import matplotlib.pyplot as plt

df_tb = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/SSI_price_for_trading_bot.csv')
df_tb.head()


df_tb['date'] = pd.to_datetime(df_tb['date'])


df_tb = df_tb.dropna()


df_tb.shape


df_tb.info()


df_tb.to_excel('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/SSI_price_cleaned.xlsx')


df_tb.set_index('date', inplace=True)


df_tb.head()


def trading_strategy(df):
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(df)):
        if df['MA5'].iloc[i] > df['MA20'].iloc[i] and df['MA5'].iloc[i-1] < df['MA20'].iloc[i-1]:
            buy_signals.append(df.index[i])  
        elif df['MA5'].iloc[i] < df['MA20'].iloc[i] and df['MA5'].iloc[i-1] > df['MA20'].iloc[i-1]:
            sell_signals.append(df.index[i])  
            
    return buy_signals, sell_signals


buy_signals, sell_signals = trading_strategy(df_tb)


print("Buy Signals:")
for signal in buy_signals:
    print(signal)

print("\nSell Signals:")
for signal in sell_signals:
    print(signal)


# Plotting
plt.figure(figsize=(12,6))
plt.plot(df_tb['close'], label='Close Price', color='blue', alpha=0.5)

# Unique labels for legend
buy_label_added = False
sell_label_added = False

# Mark the buy signals
for signal in buy_signals:
    if signal in df_tb.index:
        plt.scatter(signal, df_tb.loc[signal, 'close'], marker='o', color='green', label='Buy Signal' if not buy_label_added else '', alpha=1)
        buy_label_added = True

# Mark the sell signals
for signal in sell_signals:
    if signal in df_tb.index:
        plt.scatter(signal, df_tb.loc[signal, 'close'], marker='o', color='red', label='Sell Signal' if not sell_label_added else '', alpha=1)
        sell_label_added = True

plt.title('Stock Price with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()


import plotly.graph_objs as go
from plotly.subplots import make_subplots


fig = make_subplots(rows=1, cols=1)

# Add the closing price line
fig.add_trace(go.Scatter(
    x=df_tb.index, 
    y=df_tb['close'], 
    mode='lines', 
    name='Close Price', 
    line=dict(color='blue', width=2)))

# Add buy signals - chỉ thêm một dấu hiệu mua để tránh lặp trong chú thích
buy_trace = go.Scatter(
    x=[buy_signals[0]], 
    y=[df_tb.loc[buy_signals[0], 'close']], 
    mode='markers', 
    marker_symbol='triangle-up', 
    marker_color='green', 
    marker_size=10, 
    name='Buy Signal')
fig.add_trace(buy_trace)

# Add all buy signal points
fig.add_trace(go.Scatter(
    x=buy_signals, 
    y=df_tb.loc[buy_signals, 'close'], 
    mode='markers', 
    marker_symbol='triangle-up', 
    marker_color='green', 
    marker_size=10, 
    showlegend=False))

# Add sell signals - chỉ thêm một dấu hiệu bán
sell_trace = go.Scatter(
    x=[sell_signals[0]], 
    y=[df_tb.loc[sell_signals[0], 'close']], 
    mode='markers', 
    marker_symbol='triangle-down', 
    marker_color='red', 
    marker_size=10, 
    name='Sell Signal')
fig.add_trace(sell_trace)

# Add all sell signal points
fig.add_trace(go.Scatter(
    x=sell_signals, 
    y=df_tb.loc[sell_signals, 'close'], 
    mode='markers', 
    marker_symbol='triangle-down', 
    marker_color='red', 
    marker_size=10, 
    showlegend=False))

fig.update_layout(
    title='SSI Price with Buy and Sell Signals',
    xaxis_title='Date',
    yaxis_title='Price',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template='plotly_dark',
    xaxis_rangeslider_visible=False)  # Ẩn range slider để làm sạch biểu đồ

fig.show()

#region Portfolio Optimization with 3 stocks, high risk
#Modern Porfolio Theory


import pandas as pd
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime, timedelta


df_porfolio_3stocks_highrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_3stocks_highrisk.head()

df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.drop(['SJS', 'HCM', 'VGC', 'VNM','CTD', 'NKG', 'MWG',], axis=1)

df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.dropna()
df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.reset_index()
df_porfolio_3stocks_highrisk = df_porfolio_3stocks_highrisk.drop(['index'], axis=1)
df_porfolio_3stocks_highrisk['date'] = pd.to_datetime(df_porfolio_3stocks_highrisk['date'])

# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_3stocks_highrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()

# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_3stocks_highrisk.columns.drop('date')


# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")
#endregion

# #### Portfolio of 3 stocks with mediuma and low risk


df_porfolio_3stocks_mediumrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')

df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.drop(['SJS', 'HCM', 'VGC', 'VNM','CTD', 'NKG', 'MWG',], axis=1)

df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.dropna()
df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.reset_index()
df_porfolio_3stocks_mediumrisk = df_porfolio_3stocks_mediumrisk.drop(['index'], axis=1)
df_porfolio_3stocks_mediumrisk['date'] = pd.to_datetime(df_porfolio_3stocks_mediumrisk['date'])

# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_3stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()

# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)

tickers = df_porfolio_3stocks_mediumrisk.columns.drop('date')

# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.35) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 3 stocks with low risk
# #### Portfolio of 5 stocks with high risk


df_porfolio_optimization = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_optimization.head()


df_porfolio_optimization.isnull().sum()


df_porfolio_optimization = df_porfolio_optimization.drop(['SJS', 'HCM', 'VGC', 'VNM','CTD'], axis=1)


df_porfolio_optimization = df_porfolio_optimization.dropna()


df_porfolio_optimization = df_porfolio_optimization.reset_index()


df_porfolio_optimization = df_porfolio_optimization.drop(['index'], axis=1)


df_porfolio_optimization['date'] = pd.to_datetime(df_porfolio_optimization['date'])


df_porfolio_optimization.dtypes


df_porfolio_optimization.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_optimization.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


log_returns.isnull().sum()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
cov_matrix


# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)


# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252


# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 


# Set the risk free rate 
risk_free_rate = 0.02


def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_optimization.columns.drop('date')


# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]


# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
initial_weights


# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)


# Get optimal weights 
optimal_weights = optimized_results.x


print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize

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


df_porfolio_5stocks_mediumrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_5stocks_mediumrisk.head()


df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.drop(['SJS', 'HCM', 'VGC', 'VNM','CTD'], axis=1)


df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.dropna()
df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.reset_index()
df_porfolio_5stocks_mediumrisk = df_porfolio_5stocks_mediumrisk.drop(['index'], axis=1)
df_porfolio_5stocks_mediumrisk['date'] = pd.to_datetime(df_porfolio_5stocks_mediumrisk['date'])


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_5stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_5stocks_mediumrisk.columns.drop('date')


# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.35) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 5 stocks with low risk


df_porfolio_5stocks_lowrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_5stocks_lowrisk.head()


df_porfolio_5stocks_lowrisk.isnull().sum()


df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.drop(['SJS', 'HCM', 'VGC', 'VNM','CTD'], axis=1)


df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.dropna()
df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.reset_index()
df_porfolio_5stocks_lowrisk = df_porfolio_5stocks_lowrisk.drop(['index'], axis=1)
df_porfolio_5stocks_lowrisk['date'] = pd.to_datetime(df_porfolio_5stocks_lowrisk['date'])


df_porfolio_5stocks_lowrisk.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_5stocks_lowrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_5stocks_lowrisk.columns.drop('date')


# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.25) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with high risk


df_porfolio_10stocks_highrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_10stocks_highrisk.head()


df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.dropna()
df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.reset_index()
df_porfolio_10stocks_highrisk = df_porfolio_10stocks_highrisk.drop(['index'], axis=1)
df_porfolio_10stocks_highrisk['date'] = pd.to_datetime(df_porfolio_10stocks_highrisk['date'])


df_porfolio_10stocks_highrisk.head()


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_highrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))


log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


tickers = df_porfolio_10stocks_highrisk.columns.drop('date')


# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with medium risk


df_porfolio_10stocks_mediumrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_10stocks_mediumrisk.head()


df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.dropna()
df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.reset_index()
df_porfolio_10stocks_mediumrisk = df_porfolio_10stocks_mediumrisk.drop(['index'], axis=1)
df_porfolio_10stocks_mediumrisk['date'] = pd.to_datetime(df_porfolio_10stocks_mediumrisk['date'])


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_mediumrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()

# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)

tickers = df_porfolio_10stocks_mediumrisk.columns.drop('date')

# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.3) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")


# #### Portfolio of 10 stocks with low risk


df_porfolio_10stocks_lowrisk = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/top_stocks.csv')
df_porfolio_10stocks_lowrisk.head()


df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.dropna()
df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.reset_index()
df_porfolio_10stocks_lowrisk = df_porfolio_10stocks_lowrisk.drop(['index'], axis=1)
df_porfolio_10stocks_lowrisk['date'] = pd.to_datetime(df_porfolio_10stocks_lowrisk['date'])


# Calculate the Lognormal Returns for each stock
df_numerical = df_porfolio_10stocks_lowrisk.select_dtypes(include=[np.number])
log_returns = np.log(df_numerical / df_numerical.shift(1))

log_returns = log_returns.dropna()


# Calculate the covariance matrix using annualized log returns
cov_matrix = log_returns.cov()*252
# Calculate the porfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)
# Calculate the expected return 
def expected_return (weights, log_return):
    return np.sum(log_return.mean()*weights)*252
# Calculate the sharpe ratio
def sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return (expected_return (weights, log_return) - risk_free_rate) / standard_deviation (weights, cov_matrix) 
# Set the risk free rate 
risk_free_rate = 0.02
def neg_sharpe_ratio (weights, log_return, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)

tickers = df_porfolio_10stocks_lowrisk.columns.drop('date')

# Set the constraints and bounds
constraints = {'type' : 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.2) for _ in range(len(tickers))]
# Set the initial weights
initial_weights = np.array([1/len(tickers)]*len(tickers))
# Optimize the weights to maximize the Sharpe Ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights,args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
# Get optimal weights 
optimal_weights = optimized_results.x
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

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
portfolio_annual_return = (annual_return_ssi * weight_ssi) + \
                          (annual_return_vnd * weight_vnd) + \
                          (annual_return_hpg * weight_hpg)


portfolio_annual_return


# #### Calculate annual return of VN-INDEX


import pandas as pd
df_VN_Index_price = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Personal Items/Stock Recommendation System Project/VN_Index_price_2017_2023.csv')


df_VN_Index_price['date'] = pd.to_datetime(df_VN_Index_price['date'])


df_VN_Index_price = df_VN_Index_price.sort_values(by='date')


df_VN_Index_price = df_VN_Index_price.drop(['Unnamed: 0'], axis=1)


df_VN_Index_price['close'] = df_VN_Index_price['close'].str.replace(',', '').astype(float)


df_VN_Index_price['year'] = df_VN_Index_price['date'].dt.year

# Calculate the first and last close price for each year
annual_first_close = df_VN_Index_price.groupby('year')['close'].first()
annual_last_close = df_VN_Index_price.groupby('year')['close'].last()

# Calculate the annual return of each year
annual_returns = (annual_last_close / annual_first_close - 1) * 100

# Calculate the average annual return of each year
average_annual_return = annual_returns.mean()

print("VN-Index annual return of each year in period 2017-2023:")
print(annual_returns)
print("\nVN-Index average annual return of each year in period 2017-2023:")
print(average_annual_return)





