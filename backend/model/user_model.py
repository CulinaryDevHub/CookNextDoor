import mysql.connector
import json
from flask import jsonify
from flask_bcrypt import Bcrypt
# from app import bcrypt
import os
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

            print(self.supabase)
        except:
            print("error")

    def user_getall_model(self):
        try:
            response = self.supabase.table("customer").select("*").execute()

            if response.data:
                return json.dumps(response.data)  
            else:
                return "No data found"
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
            table_name = "vendor" if user_type == "vendor" else "customer"

            response = self.supabase.table(table_name).select("*").eq("email", email).execute()

            if response.data:
                return response.data[0]  # Return the first matching user
            return None  # User not found

        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    # def get_id_by_email(self, email):
    #     query = f"SELECT customer_id FROM Customer WHERE email = {email}"


    
    def getall_dishes(self):
        try:
            # Fetch all dishes from Supabase
            response = self.supabase.table("dishes").select("*").execute()

            # Check if data exists
            if not response.data:
                return jsonify({"dishes": [], "success": True}), 200  # Return empty list if no dishes found

            # Convert data to a list of dictionaries for JSON response
            dish_list = []
            for dish in response.data:
                dish_list.append({
                    "dish_id": dish.get("dish_id"),  # Use .get() to avoid KeyError
                    "vendor_id": dish.get("vendor_id"),
                    "dish_name": dish.get("dish_name"),
                    "description": dish.get("description"),
                    "ingredients": dish.get("ingredients"),
                    "price": str(dish.get("price", "0")),  # Convert Decimal to string for JSON serialization
                    "image_url": dish.get("image_url", ""),  # Provide empty string if None
                    "availability_status": bool(dish.get("availability_status", False))  # Convert to boolean
                })

            return jsonify({"dishes": dish_list, "success": True}), 200

        except Exception as e:
            print(f"ERROR: {str(e)}")  # Print the error for debugging
            return jsonify({"message": "Failed to retrieve dishes", "error": str(e), "success": False}), 500

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
            response = self.supabase.table("cart_items").select("dish_id, quantity").eq(
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
            # Fetch dish details from Supabase
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
        
    def get_user(self, email):
        try:
            query = "SELECT firstname, lastname, contact, address FROM Customer WHERE email=%s"
            self.cur.execute(query, (email,))
            result = self.cur.fetchone()

            return result
        
        except Exception as e:
            print(f"Error fetching cart items: {str(e)}")  # Log the error for debugging
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500