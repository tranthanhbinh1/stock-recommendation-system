from flask import Flask
from recommendation_service.stock_recommender import StockRecommender

app = Flask(__name__)

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    # Call the classes in recommendation_service here
    # For example:
    stock_recommender = StockRecommender()
    recommendation = stock_recommender.get_recommendation()

    return recommendation

if __name__ == '__main__':
    app.run()

#TODO: Authentication - Registration, Login, Logout
#TODO: Add a Industry filter to the recommendation
