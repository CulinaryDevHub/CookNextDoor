from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt
import numpy as np
import pickle 
from recommendation_module import recommend_dishes 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

@app.route("/")
def welcome():
    return 'Hello World'

with open('data_preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    input_data = request.json
    user_dish_name = input_data.get('dish_name', '')
    user_preferences = input_data.get('user_preferences', '')
    excluded_ingredients = input_data.get('excluded_ingredients', '')

    recommendations = recommend_dishes(user_dish_name, user_preferences, excluded_ingredients)

    if isinstance(recommendations, str):  
        return jsonify({"message": recommendations}), 404
    return jsonify(recommendations), 200


if __name__ == '__main__':
    app.run(debug=True)

from controller import * 
