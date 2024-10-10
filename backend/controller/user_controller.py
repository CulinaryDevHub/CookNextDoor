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
      
    access_token = create_access_token(identity=email)
    #response = {"access_token":access_token}
  
    return jsonify({
        "email": email,
        "token": access_token,
        "status": "Logged in Successfully "
    })

    # return "Login successful"