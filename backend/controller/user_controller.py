from app import app
from model.user_model import user_model
import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

obj = user_model()

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

@app.route("/user/getall")
def getall():
    return obj.user_getall_model()

@app.route("/user/addone", methods=["POST"])
def addone():
    return obj.user_addone_model(request.form)

@app.route('/user/logintoken', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
  
    if email:
        user = obj.get_user_by_email(email)
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
  
    # return jsonify({
    #     "email": email,
    #     "access_token": access_token
    # })

    return "Login successful"