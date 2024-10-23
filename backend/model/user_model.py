import mysql.connector
import json
from flask import jsonify
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

class UserModel():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost", user="root", password="J@nvi123", database="janvi")
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
                INSERT INTO vendors (user_type,email, password, firstname, lastname, contact, address)
                VALUES (%s,%s, %s, %s, %s, %s, %s);
            """
        if data['user_type'] == 'customer':
            query = """
                INSERT INTO Customer (user_type, email, password, firstname, lastname, contact, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        
        print("Query:", query)
        print("Parameters:", (
            data['user_type'],
            data['email'],
            hashed_password,
            data['firstname'],
            data['lastname'],
            data['contact'],
            data['address']
            ))
        self.cur.execute(query, (
            data['user_type'],
            data['email'],
            hashed_password,
            data['firstname'],
            data['lastname'],
            data['contact'],
            data['address']
        ))
        

        return jsonify({'message': 'User added successfully', 'success': True}), 200;


    def get_user_by_email(self, email, user_type):
        query = None
        if user_type == 'vendor':
            query = f"SELECT * FROM vendors WHERE email = '{email}'"
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
