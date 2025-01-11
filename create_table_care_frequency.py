import sys
from os.path import dirname, abspath
sys.path.append(dirname(abspath(__file__)) + '/app')
from app.db_connection.conn import get_connection

def create_care_frequency_table():
    conn = get_connection()
    if conn is None:
        raise Exception('Database connection is not established.')
        
    cursor = conn.cursor()
    
    # Define the table structure
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS care_frequency_chart (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            resident_initials VARCHAR(10),
            mattress_appropriate VARCHAR(3),
            cushion_appropriate VARCHAR(3),
            functionality_check VARCHAR(3),
            pressure_areas_checked VARCHAR(3),
            redness_present VARCHAR(3),
            position VARCHAR(10),
            incontinence_urine VARCHAR(3),
            incontinence_bowels VARCHAR(3),
            diet_intake VARCHAR(3),
            fluid_intake VARCHAR(3),
            supplement_intake VARCHAR(3),
            staff_initials VARCHAR(10),
            notes VARCHAR(100)
        )
    """
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'care_frequency_chart' created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_care_frequency_table()