from flask import Flask,request,jsonify,Response
from model.user_model import UserModel
from flask_bcrypt import Bcrypt
from routes import vendor_routes, customer_routes
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import numpy as np
import pickle
import json
from recommendation_module import recommend_dishes 
from flask_cors import CORS
import pandas as pd



app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)


CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS","PUT","DELETE"]) 

obj = UserModel()
print(f"obj: {obj}")

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@app.before_request
def log_request_info():
    print("Headers: %s", request.headers)
    print("Body: %s", request.get_data())
    
@app.route("/")
def welcome():
    return 'Hello World'

@app.route("/user/getall")
def getall():
    return obj.user_getall_model()

with open('data_preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200
    

@app.route("/api/user/addone", methods=["POST", "OPTIONS"])
def addone():
    print("addone")
    if request.method == 'OPTIONS':
        # CORS preflight request
        response =Flask.make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response
    
    data = request.get_json()  # Parse JSON from request body

    if not data:
        return jsonify({'message': 'No data provided', 'success': False}), 400  # Respond with 400 error if no data

    # Validate incoming data (e.g., check for required fields)
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password', 'success': False}), 400
    
    # return obj.user_addone_model(data)
   
    print(f"obj: {obj}")
    
    try:
        # Pass JSON data to the model function
        print(f"Data passed to user_addone_model: {data}")
        return obj.user_addone_model(data)
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Server error occurred', 'success': False}), 500



@app.route('/api/user/logintoken', methods=["POST", "OPTIONS"])
def create_token():
    user_type = request.json.get("user_type", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

  
    if email:
        user = obj.get_user_by_email(email, user_type)
    else:
        return jsonify({"error": "Email is required"}), 400
    #if email != "test" or password != "test":
    #    return {"msg": "Wrong email or password"}, 401
    if user is None:
        print("User not found or returned None")
        return jsonify({"error": "Wrong email or passwords"}), 401
      
    print(f"User found: {user}")
    if not bcrypt.check_password_hash(user['password'], password):
        print(f"Password check failed: {user['password']} != {password}")
        return jsonify({"error": "Unauthorized"}), 401

    # if not user['password'] == password:
    #     return jsonify({"error": "Invalid password"}), 401
    # Include vendor_id or customer_id based on user type
    if user_type == 'vendor':
        user_id = user.get('vendor_id')
    elif user_type == 'customer':
        user_id = user.get('customer_id')
    else:
        return jsonify({"error": "Invalid user type"}), 400
    
    access_token = create_access_token(identity=email,additional_claims={
        'user_type': user_type,
        'user_id': user_id
    })
    #response = {"access_token":access_token}
  
    return jsonify({
        "email": email,
        "token": access_token,
        "status": "Logged in Successfully "
    })

    # return "Login successful"
    
# Register API routes
app.register_blueprint(vendor_routes, url_prefix='/api/vendor')
app.register_blueprint(customer_routes, url_prefix='/api/customer')

with open('kmeans_model.pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

file_path = r'C:\Users\sahuj\Desktop\mp-main\CookNextDoor\backend\preprocessed_restaurant_data.csv'
df = pd.read_csv(file_path)

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


if __name__ == "__main__":
    app.run(debug=True)


# from controller import *