# selectfrom.py
import sys
from os.path import abspath, dirname

# Add 'app' directory to the sys.path
sys.path.append(dirname(abspath(__file__)) + '/app')

from app.db_connection.conn import get_connection

def test_db():
    conn = get_connection()
    if conn is None:
        raise Exception('Database connection is not established.')
    
    cursor = conn.cursor()
    
    # Check database connection version
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Connected to -", db_version)
    
    # Execute SELECT query
    select_query = "SELECT * FROM staff_list"
    cursor.execute(select_query)
    
    # Fetch all records from the table
    records = cursor.fetchall()
    
    # Print each record
    for record in records:
        print(record)
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    test_db()