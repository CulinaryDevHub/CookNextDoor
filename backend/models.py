from database import get_db_connection

# Get all vendors
def get_vendors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors")
    vendors = cursor.fetchall()
    connection.close()
    return vendors



# Get all dishes by vendor
def get_dishes_by_vendor(vendor_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dishes WHERE vendor_id = %s", (vendor_id,))
    dishes = cursor.fetchall()
    connection.close()
    return dishes

# Get all orders by vendor
def get_orders_by_vendor(vendor_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE vendor_id = %s", (vendor_id,))
    orders = cursor.fetchall()
    connection.close()
    return orders

# Add a new dish
def add_dish(dish_name, price, description, ingredients, vendor_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO dishes (dish_name, price, description, ingredients, vendor_id)
                   values(%s,%s,%s,%s,%s)
    """, ( dish_name, price, description, ingredients,vendor_id)) 
     # Fix the placeholders and add the description and ingredients
    connection.commit()
    connection.close()

# Update an existing dish
def update_dish(dish_id, name, price, description, ingredients):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE dishes 
    SET dish_name = %s, price = %s, description = %s, ingredients = %s
    WHERE dish_id = %s
    """, (name, price, description, ingredients, dish_id))  # Add description and ingredients to the update query
    connection.commit()
    connection.close()

# Delete a dish
def delete_dish(dish_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dishes WHERE dish_id = %s", (dish_id,))
    connection.commit()
    connection.close()