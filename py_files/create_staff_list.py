import psycopg2, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from werkzeug.security import generate_password_hash
from app.db_connection.conn import get_connection

def create_staff_list_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff_list (
            id SERIAL PRIMARY KEY,
            staff_firstname VARCHAR(100) NOT NULL,
            staff_surname VARCHAR(100) NOT NULL,
            staff_initials VARCHAR(10) NOT NULL,
            staff_unique_id VARCHAR(10) NOT NULL,
            staff_access VARCHAR(20) NOT NULL,
            staff_notes TEXT,
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    
    # Sample data with hashed passwords
    staff_data = [
        ('Cecil', 'Dundee', 'CD', 'CD01', 'family', '', generate_password_hash('password')),
        ('Peter', 'Sido', 'PS', 'PS01', 'admin', '', generate_password_hash('password')), 
        ('Alan', 'Brown', 'AB', 'AB01', 'carer', '', generate_password_hash('password'))
    ]
    
    # Insert data
    cursor.executemany("""
        INSERT INTO staff_list 
        (staff_firstname, staff_surname, staff_initials, staff_unique_id, 
         staff_access, staff_notes, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, staff_data)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("The staff_list table has been successfully created and populated.")

if __name__ == "__main__":
    create_staff_list_table()