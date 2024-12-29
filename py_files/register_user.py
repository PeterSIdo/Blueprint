from werkzeug.security import generate_password_hash
import psycopg2, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#from app.db_connection.config import Config
from app.db_connection.conn import get_connection

def register_user(firstname, surname, initials, unique_id, access, notes, password):
    # Generate a password hash
    password_hash = generate_password_hash(password)
    
    # Connect to your database
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert the new user into the database
    cursor.execute('''
        INSERT INTO staff_list (staff_firstname, staff_surname, staff_initials, staff_unique_id, staff_access, staff_notes, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (firstname, surname, initials, unique_id, access, notes, password_hash))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("User registered successfully!")

# Example usage
register_user('Alan', 'Brown', 'AB01', 'AB01', 'carer',' ', 'alanmouse')
# register_user('Peter', 'Sido', 'PS', 'PS01', 'admin',' ', 'petermouse')