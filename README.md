# Stock Recommendation System

**A stocks recommendation system, offers the following features**:

* **Portfolio Optimizer**: Given a list of stocks, the system will optimize the portfolio by calculating the optimal weights for each stock in the portfolio.
    * **Optimization Algorithms**: The system utilizes **The Modern Portfolio Theory (MPT)** or **mean-variance analysis** to optimize the portfolio.

* **Industries Ranking**: The system will rank the industries based on the average return of the stocks in the industry.

* **Stocks Recommendation**: Recommendations are made based on the following analysis:
    * **Fundamental Analysis**: Fundamental analysis of stocks are made based on calculations on:
        * **EPS (Earnings Per Share) Growth**
        * **Revenue Growth**
        * **Profit Growth**
        * **ROE (Return on Equity)**
    * **Technical Analysis**: Technical analysis of stocks are made using **Moving Average Crossover** and **Exponential Moving Average Crossover**.
    * **Industry Analysis**: Calculations on the average percent change of the stocks in each industry.

* **User Preferences**: The system will allow the user to set their preferences for the stocks recommendation, right now, this would be users' industry preferences.

* **Real-time Data**: The system will use real-time data to make recommendations

* **Real-time Trend Prediction**: The system deployed Machine Learning to make predictions on the trend of stocks in real-time.

* **Backtesting**: The portfolios will be backtesed before recommendations.
