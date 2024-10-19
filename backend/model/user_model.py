import mysql.connector
import json
from flask import jsonify
from flask_bcrypt import Bcrypt
from app import app

bcrypt = Bcrypt(app)

class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost", user="root", password="mysql@22Anshika", database="cooknextdoor")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection successful")
        except:
            print("error")

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM User")
        result=self.cur.fetchall()
        if len(result):
            return json.dumps(result)
        else:
            return "No data found"
        
    def user_addone_model(self, data):
        # self.cur.execute(f"INSERT INTO User (user_type, email, password, firstname, lastname, contact, address) values ('{data['user_type']}', '{data['email']}', '{data['password']}', '{data['firstname']}', '{data['lastname']}', '{data['contact']}', '{data['address']}');")
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Use parameterized queries to prevent SQL injection
        if data['user_type'] == 'vendor':
            query = """
                INSERT INTO Vendor (user_type, email, password, firstname, lastname, contact, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """

            self.cur.execute(query, (
            data['user_type'],
            data['email'],
            hashed_password,
            data['firstname'],
            data['lastname'],
            data['contact'],
            data['address']
            ))
            
        elif data['user_type'] == 'customer':
            query = """
                INSERT INTO Customer (user_type, email, password, firstname, lastname, contact, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        
            self.cur.execute(query, (
                data['user_type'],
                data['email'],
                hashed_password,
                data['firstname'],
                data['lastname'],
                data['contact'],
                data['address']
            ))

            # Get the `customer_id` of the newly inserted customer
            customer_id = self.cur.lastrowid  # This will get the last inserted ID for auto_increment columns

            print(f"DEBUG: Inserted customer_id: {customer_id}")
            
            # Insert the new `customer_id` into the `cart` table
            cart_query = """
                INSERT INTO cart (customer_id) VALUES (%s);
            """
            self.cur.execute(cart_query, (customer_id,))
            

        return jsonify({'message': 'User added successfully', 'success': True}), 200;


    def get_user_by_email(self, email, user_type):

        if user_type == 'vendor':
            query = f"SELECT * FROM Vendor WHERE email = '{email}'"
        if user_type == 'customer':
            query = f"SELECT * FROM Customer WHERE email = '{email}'"

        # query = f"SELECT * FROM User WHERE email = '{email}'"
        self.cur.execute(query)
        
        # Fetch the first result
        user = self.cur.fetchone()
        # print(type(user))
        
        # return jsonify(user)

        # user_data = {
        #     'user_id': user[0],
        #     'user_type': user[1],
        #     'email': user[2],
        #     'password': user[3],  # The hashed password
        #     'firstname': user[4],
        #     'lastname': user[5],
        #     'contact': user[6],
        #     'address': user[7]
        # }

        if not user:
            return None  
        return user
    
    # def get_id_by_email(self, email):
    #     query = f"SELECT customer_id FROM Customer WHERE email = {email}"


    
    def getall_dishes(self):
        try:
            # Define the SQL query
            query = """ SELECT * FROM dishes """
            
            # Execute the query
            self.cur.execute(query)
            
            # Fetch all results
            dishes = self.cur.fetchall()
            # print(dishes)

            if not dishes:
                return jsonify({"dishes": [], "success": True}), 200  # Return empty list if no dishes found
            
            # If you need to return a list of dictionaries for better JSON serialization
            dish_list = []
            for dish in dishes:

                dish_list.append({
                    "dish_id": dish['dish_id'],  # Accessing dictionary keys directly
                    "vendor_id": dish['vendor_id'],
                    "dish_name": dish['dish_name'],
                    "description": dish['description'],
                    "ingredients": dish['ingredients'],
                    "price": str(dish['price']),  # Convert Decimal to string for JSON serialization
                    "image_url": dish['image_url'] if dish['image_url'] else "",  # Provide empty string if None
                    "availability_status": bool(dish['availability_status'])  # Convert to boolean
                })
            
            return jsonify({"dishes": dish_list, "success": True}), 200
        
        except Exception as e:
            print(f"ERROR: {str(e)}")  # Print the error for debugging
            return jsonify({"message": "Failed to retrieve dishes", "error": str(e), "success": False}), 500

    def get_cart_details(self, customer_id):
        
        try:
            query = """
                SELECT dish_id, quantity FROM cart_items
                WHERE cart_id = (
                    SELECT cart_id FROM cart
                    WHERE customer_id = %s
                )
            """
            self.cur.execute(query, (customer_id,))  # Use parameterized query to prevent SQL injection

            items = self.cur.fetchall()

            item_list = [item for item in items]  # Simplified list comprehension

            return item_list
        
        except Exception as e:
            print(f"error:{str(e)}")
            return jsonify({"message": "Failed to retrieve dishes", "error": str(e), "success": False}), 500
        
    def get_dishDetails_by_dishId(self, dish_id):
        try:
            query = f"SELECT * FROM dishes WHERE dish_id = %s"
            # print("query")

            self.cur.execute(query,(dish_id,))
            # print("executed")

            dish = self.cur.fetchone()
            # print(dish)

            # if dish:
            #     dish_data = {
            #         "dish_id": dish[0],
            #         "vendor_id": dish[1],
            #         "dish_name": dish[2],
            #         "description": dish[3],
            #         "price": dish[5],
            #         "image_url": dish[6]
            #     }
            #     print(dish_data)

            return {"dish": dish, "success": True}
        
        except Exception as e :
            print(f"error:{str(e)}")
            return jsonify({"message": "Failed to retrieve dishes", "error": str(e), "success": False}), 500
        
    def get_cartId_by_custId(self, customer_id):
        try:
            query = """SELECT cart_id FROM cart WHERE customer_id = %s"""

            self.cur.execute(query,(customer_id,))

            cart_id = self.cur.fetchone()
            print(f'cart_id: {cart_id}')

            return cart_id
        
        except Exception as e :
            print(f"error:{str(e)}")
            return jsonify({"message": "Failed to retrieve cart_id", "error": str(e), "success": False}), 500  
    
    def addToCart(self, dish_id, cart_data):
        try:
            query = """
                INSERT INTO cart_items (cart_id, dish_id) VALUES (%s, %s)
            """
            cart_id = cart_data['cart_id']
            print(f"Executing query: {query} with cart_id: {cart_id}, dish_id: {dish_id}")
            self.cur.execute(query,(cart_id, dish_id,))
            self.con.commit()
            print("yes added")

            return {"message": "Dish added successfully", "success": True}

        except Exception as e:
            print(f"Error fetching cart items: {str(e)}")  # Log the error for debugging
            return jsonify({"message": "Internal Server Error", "error": str(e), "success": False}), 500