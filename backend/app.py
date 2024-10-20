from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt
import numpy as np
import pickle 
from recommendation_module import recommend_dishes 
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

@app.route("/")
def welcome():
    return 'Hello World'

with open('data_preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)


with open('kmeans_model.pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

df = pd.read_csv('C:/Users/HP/CookNextDoor/backend/preprocessed_restaurant_data.csv')

def get_current_season():
    month = datetime.now().month
    if month in [11, 12, 1, 2]:
        return 2  # Winter
    elif month in [3, 4, 5, 6]:
        return 1  # Summer
    else:
        return 0  # Rainy  

@app.route('/trends', methods=['GET'])
def get_trending_dishes():
    current_season = get_current_season()

    # Filter the dataframe by the current season
    filtered_df = df[df['Season'] == current_season]

    # Combine all clusters and get top 3 dishes for vegetarian
    veg_top3 = filtered_df[filtered_df['User_Preferences'] == 1] \
                .groupby('Dish_Name')['Quantity'].sum() \
                .nlargest(3).index.tolist()

    # Combine all clusters and get top 3 dishes for non-vegetarian
    non_veg_top3 = filtered_df[filtered_df['User_Preferences'] == 0] \
                    .groupby('Dish_Name')['Quantity'].sum() \
                    .nlargest(3).index.tolist()

    # Construct the response
    response = {
        "vegetarian": veg_top3,
        "nonvegetarian": non_veg_top3
    }

    return jsonify(response)



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



