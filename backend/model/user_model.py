import json
import os
from flask import jsonify
from flask_bcrypt import Bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class user_model():
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
        try:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            self.supabase: Client = create_client(url, key)
            print("Supabase connection established")
        except Exception as e:
            print(f"Error connecting to Supabase: {str(e)}")

    def user_getall_model(self):
        try:
            response = self.supabase.table("customer").select("*").execute()
            return json.dumps(response.data) if response.data else "No data found"
        except Exception as e:
            return f"Error fetching data: {str(e)}"

    def user_addone_model(self, data):
        try:
            # Hash the password
            hashed_password = self.bcrypt.generate_password_hash(data['password']).decode('utf-8')

            # Determine table name based on user type
            table_name = "vendor" if data["user_type"] == "cook" else "customer"

            # Insert user into the respective table
            response = self.supabase.table(table_name).insert({
                "user_type": data["user_type"],
                "email": data["email"],
                "password": hashed_password,
                "firstname": data["firstname"],
                "lastname": data["lastname"],
                "contact": data["contact"],
                "address": data["address"]
            }).execute()

            if response.data:
                if data["user_type"] == "customer":
                    customer_id = response.data[0]["customer_id"]  # Get newly created customer ID

                    # Insert customer ID into the cart table
                    self.supabase.table("cart").insert({
                        "customer_id": customer_id
                    }).execute()

                    print(f"DEBUG: Inserted customer_id: {customer_id} into cart.")

                return json.dumps({'message': 'User added successfully', 'success': True}), 200
            else:
                return json.dumps({'message': 'Failed to insert data', 'success': False, 'error': response.error}), 400

        except Exception as e:
            print(f"Error: {str(e)}")
            return json.dumps({'message': 'Server error occurred', 'success': False}), 500

    def get_user_by_email(self, email, user_type):
        try:
            table_name = "vendor" if user_type == "cook" else "customer"
            response = self.supabase.table(table_name).select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None

    def get_vendors(self):
        try:
            response = self.supabase.table("vendor").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            return []

    def get_dishes_by_vendor(self, vendor_id):
        try:
            response = self.supabase.table("dishes").select("*").eq("vendor_id", vendor_id).execute()
            return response.data if response.data else []
        except Exception as e:
            return []

    def get_orders_by_vendor(self, vendor_id):
        try:
            response = self.supabase.table("orders").select("*").eq("vendor_id", vendor_id).execute()
            return response.data if response.data else []
        except Exception as e:
            return []

    def add_dish(self, dish_name, price, description, ingredients, vendor_id):
        try:
            response = self.supabase.table("dishes").insert({
                "dish_name": dish_name,
                "price": price,
                "description": description,
                "ingredients": ingredients,
                "vendor_id": vendor_id
            }).execute()
            return response.data if response.data else None
        except Exception as e:
            return None

    def update_dish(self, dish_id, name, price, description, ingredients):
        try:
            response = self.supabase.table("dishes").update({
                "dish_name": name,
                "price": price,
                "description": description,
                "ingredients": ingredients
            }).eq("dish_id", dish_id).execute()
            return response.data if response.data else None
        except Exception as e:
            return None

    def delete_dish(self, dish_id):
        try:
            response = self.supabase.table("dishes").delete().eq("dish_id", dish_id).execute()
            return response.data if response.data else None
        except Exception as e:
            return None

    def get_cartId_by_custId(self, customer_id):
        try:
            # Fetch the cart_id for the given customer_id
            response = self.supabase.table("cart").select("cart_id").eq("customer_id", customer_id).execute()
            if not response.data:
                return None  # If no cart found, return None
            return response.data[0]["cart_id"]  # Return cart_id

        except Exception as e:
            print(f"Error fetching cart ID: {str(e)}")
            return jsonify({"message": "Failed to retrieve cart_id", "error": str(e), "success": False}), 500
        
    def get_cart_details(self, customer_id):
        try:
            cart_id = self.get_cartId_by_custId(customer_id)
            # Fetch dish_id and quantity for the given customer's cart
            response = self.supabase.table("cart_items").select("cart_item_id, dish_id, quantity").eq(
                "cart_id", cart_id
            ).execute()

            if not response.data:
                return []
            return response.data  # Returns a list of cart items

        except Exception as e:
            print(f"Error fetching cart details: {str(e)}")
            return jsonify({"message": "Failed to retrieve cart details", "error": str(e), "success": False}), 500
        
    def get_dishDetails_by_dishId(self, dish_id):
        try:
            response = self.supabase.table("dishes").select("*").eq("dish_id", dish_id).execute()

            if not response.data:
                return {"dish": None, "success": False}

            return {"dish": response.data[0], "success": True}

        except Exception as e:
            print(f"Error fetching dish details: {str(e)}")
            return {"dish": None, "success": False, "error": str(e)} 
        
    def addToCart(self, dish_id, customer_id):
        try:
            cart_id = self.get_cartId_by_custId(customer_id)
            if not cart_id:
                return jsonify({"message": "Cart not found for the customer", "success": False}), 400

            # Insert dish into the cart_items table
            response = self.supabase.table("cart_items").insert({"cart_id": cart_id, "dish_id": dish_id}).execute()

            if response.data:
                return {"message": "Dish added successfully", "success": True}, 200
            else:
                return {"message": "Failed to add dish", "success": False}, 500

        except Exception as e:
            print(f"Error adding dish to cart: {str(e)}")
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500
        
    def removeFromCart(self, customer_id, dish_id):
        try:
            cart_id = self.get_cartId_by_custId(customer_id)
            if cart_id is None:
                return jsonify({"message": "Cart not found", "success": False}), 404
            
            response = self.supabase.table("cart_items").delete().eq("cart_id", cart_id).eq("dish_id", dish_id).execute()

            if response.data is not None:
                return jsonify({"message": "Dish deleted successfully", "success": True}), 200
            else:
                return jsonify({"message": "Failed to delete dish from cart", "success": False}), 500

        except Exception as e:
            print(f"Error deleting cart items: {str(e)}")  # Log the error for debugging
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500
    
    def get_vendorId_by_dishId(self, dish_id):
        try:
            response = self.supabase.table("dishes").select("vendor_id").eq("dish_id", dish_id).execute()
            if not response.data:
                return None  # If no cart found, return None
            return response.data[0]["vendor_id"]  # Return cart_id

        except Exception as e:
            print(f"Error fetching vendor ID: {str(e)}")
            return jsonify({"message": "Failed to retrieve vendor_id", "error": str(e), "success": False}), 500
        
    def get_address_by_custId(self, customer_id):
        try:
            response = self.supabase.table("customer").select("address").eq("customer_id", customer_id).execute()
            if not response.data:
                return None
            return response.data[0]["address"]
        except Exception as e:
            print(f"Error fetching address: {str(e)}")
            return jsonify({"message": "failed to retrieve address", "error": str(e), "success": False}), 500
    
    def update_qty(self, cart_id, items):
        try:
            for item in items:
                dish_id = item["dish_id"]
                new_qty = item["qty"]
                response = self.supabase.table("cart_items").update({"quantity": new_qty}) \
                    .eq("cart_id", cart_id) \
                    .eq("dish_id", dish_id) \
                    .execute()
            if response.data:
                return {"message": "quantity updated successfully", "success": True}, 200
            else:
                return {"message": "Failed to update qty", "success": False}, 500
            
        except Exception as e:
            print(f"error updating quantity: {str(e)}")
            return jsonify({"message": "failed to update quantity", "error": str(e), "success": False}), 500
        
    def add_order(self, customer_id, vendor_id, dish_id, qty, total_price, address):
        try:
            response = self.supabase.table("orders").insert({
                "customer_id": customer_id,
                "vendor_id": vendor_id,
                "dish_id": dish_id,
                "quantity": qty,
                "total_price": total_price,
                "delivery_address": address
            }).execute()

            if response.get("error"):
                print(f"Supabase insert error: {response['error']}")
                return {"message": "Failed to add order", "error": response["error"], "success": False}, 500
        
            if response.data:
                return {"message": "order added successfully", "success": True}, 200
            else:
                return {"message": "Failed to add order", "success": False}, 500
        
        except Exception as e:
            print(f"error adding order: {str(e)}")
            return jsonify({"message": "failed to add order", "error": str(e), "success": False}), 500