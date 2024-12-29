# test_db_connection.py

import psycopg2, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db_connection.conn import get_connection

def test_db_connection():
    try:
        # Establish the connection
        connection = get_connection()
        cursor = connection.cursor()
        
        # Execute a simple query to test the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print(f"Connected to the database. PostgreSQL version: {db_version}")
        
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        
    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == '__main__':
    test_db_connection()