import base64
import io
import logging
import urllib

import pandas as pd

# from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config.logging_config import setup_logging
from recommendation_service.backtester import Backtester
from recommendation_service.main import main
from utils.timescale_connector import TimescaleConnector, TimescaleConnnector2

setup_logging()
load_dotenv()
app = Flask(__name__)
# CORS(app)


@app.route("/data/price", methods=["GET"])
def get_price():
    symbol = request.args.get("symbol", "SSI")
    df = TimescaleConnnector2.query_update_price(symbol=symbol)
    change = TimescaleConnnector2.query_update_change(symbol=symbol).index
    processed_df = pd.DataFrame(
        {
            "code": df["symbol"],
            "open": df["open"],
            "high": df["high"],
            "low": df["low"],
            "close": df["close"],
            "volume": df["vol"],
            "trend": change.astype(int),
        }
    )
    return jsonify(processed_df.to_dict(orient="records"))  # Return list directly


@app.route("/recommendation/customize/portfolio", methods=["GET"])
def get_recommendation_custom_portfolio():
    sectors = request.args.get("sectors")
    if sectors:
        sectors = sectors.split(",")
    else:
        sectors = []
    risk_level = request.args.get("risk_level", "Low")
    logging.info(f"sectors: {sectors}")
    logging.info(f"risk_level: {risk_level}")
    recommended_stock, optimal_portfolio = main(sectors, risk_level)
    recommended_stock_dict = recommended_stock.to_dict(orient="records")
    return {
        "recommended_stock": optimal_portfolio,
    }


@app.route("/recommendation/customize/ranked_stocks", methods=["GET"])
def get_recommendation_custom_recommended_stock():
    sectors = request.args.get("sectors")
    if sectors:
        sectors = sectors.split(",")
    else:
        sectors = []
    risk_level = request.args.get("risk_level", "Low")
    logging.info(f"sectors: {sectors}")
    logging.info(f"risk_level: {risk_level}")
    recommended_stock, optimal_portfolio = main(sectors, risk_level)
    recommended_stock_dict = recommended_stock.to_dict(orient="records")
    return {
        "recommended_stock": recommended_stock_dict,
    }


@app.route("/recommendation/default/portfolio", methods=["GET"])
def get_recommendation_portfolio():
    recommended_stock, optimal_portfolio = main()
    optimal_portfolio_dict = optimal_portfolio
    return {
        "optimal_portfolio": optimal_portfolio_dict,
    }


@app.route("/recommendation/default/ranked_stocks", methods=["GET"])
def get_recommendation_recommended_stock():
    recommended_stock, optimal_portfolio = main()
    recommended_stock_dict = recommended_stock.to_dict(orient="records")
    return {
        "ranked_stocks": recommended_stock_dict,
    }


@app.route("/backtest/result", methods=["GET"])
def get_backtest_result():
    symbol = request.args.get("symbol", "SSI")
    backtester = Backtester(symbol=symbol)
    output = backtester.get_backtest_summary()
    output_dict = output
    return jsonify({"output": output_dict})


@app.route("/backtest/sells_buys", methods=["GET"])
def get_backtest_sells_buys():
    symbol = request.args.get("symbol", "SSI")
    backtester = Backtester(symbol=symbol)
    trades = backtester.get_backtest_sells_buys()
    trades_dict = trades
    return jsonify({"trades": trades_dict})


# #TODO: this actually needs more time to fix
# @app.route("/backtest/plot", methods=["GET"])
# def get_backtest_plot():
#     # Run the backtest
#     backtester = Backtester()
#     backtester.get_backtest_plot()

#     # Convert the plot to a PNG image
#     img = io.BytesIO()
#     backtester.plot.savefig(img, format="png")
#     img.seek(0)

#     # Convert the PNG image to a data URL
#     plot_url = urllib.parse.quote(base64.b64encode(img.read()))

#     # Return the plot URL in the response
#     return jsonify({"plot_url": plot_url})


if __name__ == "__main__":
    app.run(debug=True)
