from database import create_tables

def initialize_database():
    create_tables()
    print("Database initialized with tables and seeded data.")

if __name__ == "__main__":
    initialize_database()
