
# from app import app
from model.user_model import user_model
import json
from flask import Flask, request, jsonify, Response, Blueprint
# from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
# from flask_bcrypt import Bcrypt
# from dotenv import load_dotenv
# import os
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt_identity, get_jwt

# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS", "DELETE"]) 


# load_dotenv()
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# jwt = JWTManager(app)

# bcrypt = Bcrypt(app)

def create_user_blueprint(bcrypt, jwt):
    user_bp = Blueprint("user", __name__)
    # vendor_routes = Blueprint('vendor_routes', __name__)
    # customer_routes = Blueprint('customer_routes', __name__)


    obj = user_model(bcrypt)

    @user_bp.route("/user")
    def hello():
        return 'Hello'

    @user_bp.route("/user/getall")
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
        
    @user_bp.before_request
    def before_request():
        headers = {'Access-Control-Allow-Origin': '*',
                   'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                   'Access-Control-Allow-Headers': 'Content-Type'}
        if request.method.lower() == 'options':
            return jsonify(headers), 200

    @user_bp.route("/api/user/addone", methods=["POST", "OPTIONS"])
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
            return jsonify({'message': 'Missing email or password', 'success': False}), 400
        

        try:
            # Pass JSON data to the model function
            response, status_code = obj.user_addone_model(data)
            return jsonify(json.loads(response)), status_code
        except Exception as e:
            # Log the error for debugging
            print(f"Error: {str(e)}")
            return jsonify({'message': 'Server error occurred', 'success': False}), 500

    @user_bp.route('/api/user/logintoken', methods=["POST", "OPTIONS"])
    def create_token():
        try:
            data = request.get_json()
            user_type = data.get("user_type")
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400

            user = obj.get_user_by_email(email, user_type)

            if not user:
                print("User not found")
                return jsonify({"success": False, "error": "Invalid email or password"}), 401

            print(f"User found: {user}")

            # Verify the password
            if not bcrypt.check_password_hash(user['password'], password):
                print(f"Password check failed: {user['password']} != {password}")
                return jsonify({"success": False, "error": "Unauthorized"}), 401

            # Generate JWT token
            user_id_field = "vendor_id" if user_type == "cook" else "customer_id"

            additional_claims = {"user_type": user_type}
            if user_type == "cook":
                additional_claims["vendor_id"] = user["vendor_id"]
            else :
                additional_claims["customer_id"] = user["customer_id"]

            access_token = create_access_token(identity=str(user[user_id_field]), additional_claims=additional_claims)


            return jsonify({
                "success": True,
                "email": email,
                "token": access_token,
                "status": "Logged in Successfully"
            })

        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({"error": "Server error occurred"}), 500

        # return "Login successful"

    @user_bp.route('/api/dishes', methods=['GET'])
    def get_dishes():
        return obj.getall_dishes() # Replace `your_class_instance` with your actual instance

    @user_bp.route(f'/api/cart/<int:customer_id>', methods=['GET'])
    @jwt_required()
    def get_cart_items(customer_id):
        if customer_id is None:
            return jsonify({"message": "customer_id is required", "success": False}), 400

        try:
            cart_items = obj.get_cart_details(customer_id)  # Get cart items from Supabase

            dish_details = []
            for item in cart_items:
                dish_id = item["dish_id"]
                quantity = item["quantity"]

                dish_data = obj.get_dishDetails_by_dishId(dish_id)  # Fetch dish details

                if dish_data["success"]:  # Only add successful dish details
                    dish_details.append({
                        "details": dish_data["dish"],
                        "quantity": quantity
                    })
            print(dish_details)
            return jsonify({"dish_details": dish_details, "success": True}), 200

        except Exception as e:
            print(f"Error fetching cart items: {str(e)}")
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500
        
    @user_bp.route('/api/cart/add', methods=['POST', 'OPTIONS'])
    @jwt_required()
    def add_to_cart():
        try:
            data = request.get_json()
            dish_id = data.get('dish_id')
            customer_id = data.get('customer_id')

            if not customer_id or not dish_id:
                return jsonify({"message": "customer_id is required", "success": False}), 400

            # Add the dish to the cart
            result, status_code = obj.addToCart(dish_id, customer_id) 

            return jsonify(result), status_code

        except Exception as e:
            print(f"Error adding to cart: {str(e)}")  # Log the error
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500 
        
    @user_bp.route('/api/cart/remove', methods=['DELETE'])
    @jwt_required()
    def remove_from_cart():
        try:
            data = request.get_json()  # Get the JSON data from the request body
            dish_id = data.get('dish_id')  # Fetch the dish_id
            customer_id = data.get('customer_id')
            # print(f"Request data: {data}") 

            if customer_id is None:
                return jsonify({"message": "customer_id is required", "success": False}), 400
            

            result = obj.removeFromCart(customer_id, dish_id)

            return result
        
        except Exception as e:
            print(f"Error deleting cart items details: {str(e)}")  # Log the error for debugging
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500  


    @user_bp.route('/api/checkEmail', methods=['POST'])
    def check_email():
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400

        try:
            result = obj.get_user(email)

            if result:
                # Debugging log: Print fetched result (for debugging purposes)
                print(f"Fetched result from DB: {result}")

                # Combine firstname and lastname into full name
                result['name'] = f"{result['firstname']} {result['lastname']}"
                del result['firstname'], result['lastname']  # Remove separate first/last names from response
                return jsonify(result)
            else:
                return jsonify({"error": "Email not found , Verify again OR Register Yourself"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500  
        
        
    
    @user_bp.route('/menu', methods=['GET'])
    @jwt_required()
    def get_vendor_menu():
        claims = get_jwt()  # Extract all claims from JWT
        jwt_vendor_id = get_jwt_identity()  # Extract vendor_id
        
        # Check if user_type is 'cook'
        if claims.get('user_type') != 'cook':
            return jsonify({"error": "Unauthorized access"}), 403

        dishes = obj.get_dishes_by_vendor(jwt_vendor_id)
        return jsonify(dishes)


    # to be changed

    @user_bp.route('/orders', methods=['GET'])
    @jwt_required()
    def get_vendor_orders():

        claims = get_jwt()
        vendor_id = int(get_jwt_identity())
        # Ensure the vendor is accessing their own orders
        if claims['user_type'] != 'cook' or claims['vendor_id'] != vendor_id:
            return jsonify({"error": "Unauthorized access"}), 403
        
        orders = obj.get_orders_by_vendor(vendor_id)
        return jsonify(orders)
    

    from flask_jwt_extended import get_jwt_identity

    @user_bp.route('/menu/add', methods=['POST'])
    @jwt_required()
    def add_new_dish():
        vendor_id = get_jwt_identity()  # Extract vendor_id directly from the token

        data = request.json
        print(data)

        obj.add_dish(
            data['dish_name'], 
            data['price'],
            data['description'], 
            data['ingredients'],
            vendor_id  
        )

        return jsonify({'message': 'Dish added successfully!'})
    

    @user_bp.route('/menu/update/<int:dish_id>', methods=['PUT'])
    @jwt_required()
    def update_existing_dish(dish_id):
        if request.method == 'OPTIONS':
            # CORS preflight request
            response =Flask.make_response()
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Methods'] = 'PUT'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            return response
        claims = get_jwt()
        if claims['user_type'] != 'vendor':
            return jsonify({"error": "Unauthorized access"}), 403
        data = request.json
        print(data)
    
        obj.update_dish(
            dish_id, 
            data['dish_name'], 
            data['price'], 
            data['description'], 
            data['ingredients']
        )
        return jsonify({'message': 'Dish updated successfully!'})
    

    @user_bp.route('/menu/delete/<int:dish_id>', methods=['DELETE'])
    @jwt_required()
    def delete_dish_route(dish_id):
        if request.method == 'OPTIONS':
            # CORS preflight request
            response =Flask.make_response()
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Methods'] = 'DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            return response
        claims = get_jwt()
        if claims['user_type'] != 'vendor':
            return jsonify({"error": "Unauthorized access"}), 403

        obj.delete_dish(dish_id)
        return jsonify({'message': 'Dish deleted successfully!'})

    @user_bp.route('/vendors', methods=['GET'])
    # @jwt_required()
    def get_all_vendors():
        vendors = obj.get_vendors()
        return jsonify(vendors)
    


    @user_bp.route('/vendor/menu/<int:vendor_id>', methods=['GET'])
    # @jwt_required()
    def get_vendor_menu_for_customer(vendor_id):
        dishes = obj.get_dishes_by_vendor(vendor_id)
        return jsonify(dishes)

    @user_bp.route('/order/add', methods=['POST', "OPTION"])
    @jwt_required()
    def place_order():
        claims = get_jwt()
        customer_id = int(get_jwt_identity())
        if claims['user_type'] != 'customer' or claims['customer_id'] != customer_id:
            return jsonify({"error": "Unauthorized access"}), 403
        
        cart_id = obj.get_cartId_by_custId(customer_id)

        data = request.get_json()
        address = data.get("address")
        items = data.get("items")
        obj.update_qty(cart_id, items)

        cart_details = obj.get_cart_details(customer_id)
        for detail in cart_details:
            dish_id = detail['dish_id']
            qty = detail['quantity']
            dish_details = obj.get_dishDetails_by_dishId(dish_id)
            vendor_id = dish_details['dish']['vendor_id']
            total_price = dish_details['dish']['price'] * qty

            obj.add_order(customer_id, vendor_id, dish_id, qty, total_price, address)

        return jsonify({'message': 'order confirmed'})
    

    return user_bp





