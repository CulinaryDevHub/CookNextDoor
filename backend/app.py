from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS"]) 

@app.route("/")
def welcome():
    return "Hello World"

user_data = {
    "name": "Rachel Green",
    "address": "123 Main St, Anytown",
    "phone": "957-456-7890"
}

def get_cart_data():
    cart_data = {
        "items": [
            {"name": "Pizza", "quantity": 3, "price": 100},
            {"name": "Burger", "quantity": 2, "price": 50},
            {"name": "Noodles", "quantity": 3, "price": 70},
            {"name": "Crispy-Veg", "quantity": 2, "price": 90}
        ]
    }

    # Calculate the total price based on quantity and price
    cart_data["totalPrice"] = sum(item["quantity"] * item["price"] for item in cart_data["items"])
    
    return cart_data

# Fetching the cart data
cart_data = get_cart_data()
print(cart_data)

@app.route('/api/getUserDetails', methods=['GET'])
def get_user_details():
    return jsonify(user_data)

@app.route('/api/getCartItems', methods=['GET'])
def get_cart_items():
    return jsonify(cart_data)

if __name__ == '__main__':
    app.run(debug=True)
