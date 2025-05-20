# from flask import Blueprint, jsonify, request,Flask
# from models import get_vendors, get_dishes_by_vendor, get_orders_by_vendor, add_dish, update_dish, delete_dish
# from flask_jwt_extended import jwt_required, get_jwt

# vendor_routes = Blueprint('vendor_routes', __name__)
# customer_routes = Blueprint('customer_routes', __name__)

# Vendor API
# @vendor_routes.route('/info/<int:vendor_id>', methods=['GET'])
# @jwt_required
# def get_vendor_info(vendor_id):
#     claims = get_jwt()
#     if claims['user_type'] != 'vendor' or claims['user_id'] != vendor_id:
#         return jsonify({"error": "Unauthorized access"}), 403
#     vendor = get_vendors(vendor_id)
#     return jsonify(vendor)

# @vendor_routes.route('/menu/<int:vendor_id>', methods=['GET'])
# @jwt_required()
# def get_vendor_menu(vendor_id):
#     claims = get_jwt()
#     # Ensure the vendor is accessing their own menu
#     if claims['user_type'] != 'vendor' or claims['user_id'] != vendor_id:
#         return jsonify({"error": "Unauthorized access"}), 403
#     dishes = get_dishes_by_vendor(vendor_id)
#     return jsonify(dishes)

# @vendor_routes.route('/orders/<int:vendor_id>', methods=['GET'])
# @jwt_required()
# def get_vendor_orders(vendor_id):

#     claims = get_jwt()
#     # Ensure the vendor is accessing their own orders
#     if claims['user_type'] != 'vendor' or claims['user_id'] != vendor_id:
#         return jsonify({"error": "Unauthorized access"}), 403
    
#     orders = get_orders_by_vendor(vendor_id)
#     return jsonify(orders)

# Add a new dish
# @vendor_routes.route('/menu/add', methods=['POST'])
# @jwt_required()
# def add_new_dish():

#     claims = get_jwt()
    
    
#     vendor_id = claims['user_id']
    
    
#     if claims['user_type'] != 'vendor':
#         return jsonify({"error": "Unauthorized access"}), 403
    
#     data = request.json
#     print(data)
   
    
#     add_dish(
#         data['dish_name'], 
#         data['price'],
#         data['description'], 
#         data['ingredients'],
#         vendor_id
#     )
#     return jsonify({'message': 'Dish added successfully!'})

# Update an existing dish
# @vendor_routes.route('/menu/update/<int:dish_id>', methods=['PUT'])
# @jwt_required()
# def update_existing_dish(dish_id):
#     if request.method == 'OPTIONS':
#         # CORS preflight request
#         response =Flask.make_response()
#         response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#         response.headers['Access-Control-Allow-Methods'] = 'PUT'
#         response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#         return response
#     claims = get_jwt()
#     if claims['user_type'] != 'vendor':
#         return jsonify({"error": "Unauthorized access"}), 403
#     data = request.json
#     print(data)
  
#     update_dish(
#         dish_id, 
#         data['dish_name'], 
#         data['price'], 
#         data['description'], 
#         data['ingredients']
#     )
#     return jsonify({'message': 'Dish updated successfully!'})

# Delete a dish
# @vendor_routes.route('/menu/delete/<int:dish_id>', methods=['DELETE'])
# @jwt_required()
# def delete_dish_route(dish_id):
#     if request.method == 'OPTIONS':
#         # CORS preflight request
#         response =Flask.make_response()
#         response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#         response.headers['Access-Control-Allow-Methods'] = 'DELETE'
#         response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#         return response
#     claims = get_jwt()
#     if claims['user_type'] != 'vendor':
#         return jsonify({"error": "Unauthorized access"}), 403

#     delete_dish(dish_id)
#     return jsonify({'message': 'Dish deleted successfully!'})

# # Customer API
# @customer_routes.route('/vendors', methods=['GET'])
# @jwt_required()
# def get_all_vendors():
#     vendors = get_vendors()
#     return jsonify(vendors)

# @customer_routes.route('/vendor/menu/<int:vendor_id>', methods=['GET'])
# @jwt_required()
# def get_vendor_menu_for_customer(vendor_id):
#     dishes = get_dishes_by_vendor(vendor_id)
#     return jsonify(dishes) 