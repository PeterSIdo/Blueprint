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
            """
            CREATE TABLE IF NOT EXISTS bowel_list(
                id SERIAL PRIMARY KEY,
                bowel_type VARCHAR(10) NOT NULL,
                bowel_size VARCHAR(10) NOT NULL,
                bowel_mode VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fluid_list(
                id SERIAL PRIMARY KEY,
                fluid_name VARCHAR(50) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS food_list(
                id SERIAL PRIMARY KEY,
                food_name VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS personal_care_list(
                id SERIAL PRIMARY KEY,
                personal_care_name VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS report_list(
                id SERIAL PRIMARY KEY,
                report_name VARCHAR(50) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resident_list(
                id SERIAL PRIMARY KEY,
                resident_firstname VARCHAR(50) NOT NULL,
                resident_surname VARCHAR(50) NOT NULL,
                resident_unit VARCHAR(50) NOT NULL,
                resident_room VARCHAR(10) NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                resident_unique_id VARCHAR(100) NOT NULL,
                resident_notes TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS service_list(
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS staff_list(
                id SERIAL PRIMARY KEY,
                staff_firstname VARCHAR(50) NOT NULL,
                staff_surname VARCHAR(50) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL,
                staff_access VARCHAR(20) NOT NULL,
                staff_username VARCHAR(20) NOT NULL,
                staff_email VARCHAR(20) NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS unit_list(
                id SERIAL PRIMARY KEY,
                unit_name VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bowel_chart(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                bowel_type VARCHAR(10) NOT NULL,
                bowel_size VARCHAR(10) NOT NULL,
                bowel_mode VARCHAR(50) NOT NULL,
                bowel_note VARCHAR(100) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS cardex_chart(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                cardex_text VARCHAR(1000) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS care_frequency_chart (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10),
                mattress_appropriate VARCHAR(5),
                cushion_appropriate VARCHAR(5),
                functionality_check VARCHAR(5),
                pressure_areas_checked VARCHAR(5),
                redness_present VARCHAR(5),
                incontinence_urine VARCHAR(5),
                incontinence_bowels VARCHAR(5),
                diet_intake VARCHAR(5),
                fluid_intake VARCHAR(5),
                supplement_intake VARCHAR(5),
                staff_initials VARCHAR(10),
                notes VARCHAR(10)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fluid_chart(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                fluid_name VARCHAR(100) NOT NULL,
                fluid_volume VARCHAR(100) NOT NULL,
                fluid_note VARCHAR(100) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS food_chart(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                food_name VARCHAR(100) NOT NULL,
                food_amount VARCHAR(10) NOT NULL,
                food_note VARCHAR(100) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS personal_care_chart(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                resident_initials VARCHAR(10) NOT NULL,
                personal_care_type VARCHAR(100) NOT NULL,
                personal_care_duration VARCHAR(10) NOT NULL,
                personal_care_note VARCHAR(100) NOT NULL,
                staff_initials VARCHAR(10) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS staff_log (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                entry_category VARCHAR(50),
                description VARCHAR(1000),
                suggested_completion_time TIMESTAMPTZ,
                initiator VARCHAR(50),
                completer VARCHAR(50),
                task_completed BOOLEAN DEFAULT false
            );
            """
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