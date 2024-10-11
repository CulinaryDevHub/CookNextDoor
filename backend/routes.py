from flask import Blueprint, jsonify, request
from models import get_vendors, get_dishes_by_vendor, get_orders_by_vendor, add_dish, update_dish, delete_dish

vendor_routes = Blueprint('vendor_routes', __name__)
customer_routes = Blueprint('customer_routes', __name__)

# Vendor API
@vendor_routes.route('/info/<int:vendor_id>', methods=['GET'])
def get_vendor_info(vendor_id):
    vendor = get_vendors(vendor_id)
    return jsonify(vendor)

@vendor_routes.route('/menu/<int:vendor_id>', methods=['GET'])
def get_vendor_menu(vendor_id):
    dishes = get_dishes_by_vendor(vendor_id)
    return jsonify(dishes)

@vendor_routes.route('/orders/<int:vendor_id>', methods=['GET'])
def get_vendor_orders(vendor_id):
    orders = get_orders_by_vendor(vendor_id)
    return jsonify(orders)

# Add a new dish
@vendor_routes.route('/menu/add', methods=['POST'])
def add_new_dish():
    data = request.json
    print(data)
    # Now passing description and ingredients as well
    add_dish(
        data['dish_name'], 
        data['price'], 
        data['description'], 
        data['ingredients'], 
        data['vendor_id']
    )
    return jsonify({'message': 'Dish added successfully!'})

# Update an existing dish
@vendor_routes.route('/menu/update/<int:dish_id>', methods=['PUT'])
def update_existing_dish(dish_id):
    data = request.json
    print(data)
    # Now passing description and ingredients for update
    update_dish(
        dish_id, 
        data['dish_name'], 
        data['price'], 
        data['description'], 
        data['ingredients']
    )
    return jsonify({'message': 'Dish updated successfully!'})

# Delete a dish
@vendor_routes.route('/menu/delete/<int:dish_id>', methods=['DELETE'])
def delete_dish_route(dish_id):
    delete_dish(dish_id)
    return jsonify({'message': 'Dish deleted successfully!'})

# Customer API
@customer_routes.route('/vendors', methods=['GET'])
def get_all_vendors():
    vendors = get_vendors()
    return jsonify(vendors)

@customer_routes.route('/vendor/menu/<int:vendor_id>', methods=['GET'])
def get_vendor_menu_for_customer(vendor_id):
    dishes = get_dishes_by_vendor(vendor_id)
    return jsonify(dishes)
