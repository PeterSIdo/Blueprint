import psycopg2

def get_connection_nb():
    try:
        connection = psycopg2.connect(
            dbname='care6',
            user='postgres',
            password='jelszo',
            host='34.105.189.70',
            port='5432'
        )
        return connection
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None

def create_tables():
    connection = get_connection_nb()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        # List of SQL statements to create tables
        create_table_queries = [
        '''
        CREATE TABLE IF NOT EXISTS admin_list(
            id SERIAL NOT NULL,
            admin_firstname varchar(100) NOT NULL,
            admin_surname varchar(100) NOT NULL,
            admin_initials varchar(10) NOT NULL,
            admin_unique_id varchar(10) NOT NULL,
            admin_access varchar(20) NOT NULL,
            admin_notes text,
            password_hash varchar(255) NOT NULL,
            PRIMARY KEY(id)
            ); '''
        ]

        # Execute each SQL statement to create tables
        for query in create_table_queries:
            cursor.execute(query)

        # Commit the changes
        connection.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_tables()