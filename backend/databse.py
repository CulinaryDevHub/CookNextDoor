import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="J@nvi123",
        database="janvi"
    )
    print("connection done")
    return connection
connection = get_db_connection()


def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create Vendors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        password_hash VARCHAR(255),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        contact_number VARCHAR(20),
        address_id INT(11)
    )
    """)

    # Create Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        password_hash VARCHAR(255),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        contact_number VARCHAR(20),
        address_id INT(11)
    )
    """)

    # Create Dishes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        dish_id INT AUTO_INCREMENT PRIMARY KEY,
        vendor_id INT,
        dish_name VARCHAR(255),
        description TEXT,
        ingredients TEXT,
        price DECIMAL(10,2),
        image_url VARCHAR(255),
        availability_status TINYINT(1),
        FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
    )
    """)

    # Create Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        vendor_id INT,
        dish_id INT,
        quantity INT,
        total_price DECIMAL(10,2),
        delivery_address_id INT,
        placed_at TIMESTAMP,
        delivered_at TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id),
        FOREIGN KEY (dish_id) REFERENCES dishes(dish_id)
    )
    """)

    connection.commit()
    connection.close()
