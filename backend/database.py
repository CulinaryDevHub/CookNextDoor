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
        user_type ENUM('vendor', 'customer') NOT NULL,
        email VARCHAR(255),
        password VARCHAR(255),
        firstname VARCHAR(100),
        lastname VARCHAR(100),
        contact VARCHAR(20),
        address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_type ENUM('vendor', 'customer') NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    contact VARCHAR(10),
    address TEXT
);    
    """
)

   

    # Create Dishes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        dish_id INT AUTO_INCREMENT PRIMARY KEY,
        vendor_id INT NOT NULL,
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
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
        FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id),
        FOREIGN KEY (dish_id) REFERENCES dishes(dish_id)
    )
    """)



    connection.commit()
    connection.close()
