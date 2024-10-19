from app import app
from model.user_model import user_model
import json
from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from flask_cors import CORS

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS"]) 

obj = user_model()

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

@app.route("/user/getall")
def getall():
    return obj.user_getall_model()

# @app.after_request
# def after_request(response):
#     origin = request.headers.get("Origin")
#     if origin in ALLOWED_ORIGIN:
#         response.headers.add("Access-Control-Allow-Origin", origin)
#     else:
#         response.header.add("Access-Control-Allow-Origin", "null")
#     response.header.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
#     response.header.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
#     return response
    
@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

@app.route("/api/user/addone", methods=["POST", "OPTIONS"])
def addone():
    if request.method == 'OPTIONS':
        # CORS preflight request
        response = Flask.make_response()
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
    try:
        # Pass JSON data to the model function
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
    if user["user_type"] == "customer":  
        access_token = create_access_token(identity=user['customer_id'])
    elif user["user_type"] == "vendor":  
        access_token = create_access_token(identity=user['vendor_id'])
    #response = {"access_token":access_token}
  
    return jsonify({
        "email": email,
        "token": access_token,
        "status": "Logged in Successfully "
    })

    # return "Login successful"

@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    return obj.getall_dishes()  # Replace `your_class_instance` with your actual instance

@app.route(f'/api/cart/<int:customer_id>', methods=['GET'])
def get_cart_items(customer_id):
    # customer_id = request.args.get("customer_id", None)  # Fetch customer_id from query params
    if customer_id is None:
        return jsonify({"message": "customer_id is required", "success": False}), 400

    try:
        dishes = obj.get_cart_details(customer_id)  # Assuming this method returns valid cart details
        # print(type(dishes))
        # print(dishes)

        dish_details = []
        for dish in dishes:
            # print(dish['dish_id'])
            details = obj.get_dishDetails_by_dishId(dish["dish_id"])  # 'details' is a dict, not a Response now
            if details["success"]:  # Ensure we only add successful dish details
                dish_details.append(details)

        # print(type(dish_details))
        
        return jsonify({"dish_details": dish_details, "success": True}),200
    except Exception as e:
        print(f"Error fetching cart items: {str(e)}")  # Log the error for debugging
        return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500
    
@app.route('/api/cart/add', methods=['POST', 'OPTIONS'])
def add_to_cart():
    # customer_id = request.args.get("customer_id", None)  # Fetch customer_id from query params
    
    
    # print(customer_id)
    
    try:
        data = request.get_json()  # Get the JSON data from the request body
        dish_id = data.get('dish_id')  # Fetch the dish_id
        customer_id = data.get('customer_id')
        print(f"Request data: {data}") 

        if customer_id is None:
            return jsonify({"message": "customer_id is required", "success": False}), 400
        
        cart_id = obj.get_cartId_by_custId(customer_id)
        print(cart_id)

        result = obj.addToCart(dish_id, cart_id)  # Call the function that adds the dish to the cart
        print(type(result))
        if isinstance(result, dict) and result.get('success'):  # Ensure result is a dictionary
            return jsonify(result), 200  # Return a success response
        else:
            return jsonify(result), 500   # Handle any errors from the function
        # return jsonify({'dish_id': dish_id, 'cart_id': cart_id, 'success': True}), 200;

    except Exception as e:
        print(f"Error fetching cart items details: {str(e)}")  # Log the error for debugging
        return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500    