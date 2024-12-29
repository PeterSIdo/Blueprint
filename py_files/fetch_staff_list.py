import psycopg2, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.db_connection.conn import get_connection

def fetch_and_print_staff_list():
    try:
        # Establish a connection to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Execute a query to fetch all data from the staff_list table
        cursor.execute("SELECT * FROM staff_list")

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the column names
        column_names = [desc[0] for desc in cursor.description]
        print("\t".join(column_names))

        # Print each row
        for row in rows:
            print("\t".join(map(str, row)))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    fetch_and_print_staff_list()