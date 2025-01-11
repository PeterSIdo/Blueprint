# create_table.py
import sys
from os.path import dirname, abspath
import csv

# Add the path to the db_connection module
sys.path.append(dirname(abspath(__file__)) + '/app')

from app.db_connection.conn import get_connection


def create_table(table_name, column_names):
    conn = get_connection()
    if conn is None:
        raise Exception('Database connection is not established.')

    cursor = conn.cursor()

    # Exclude 'id' if it exists in column names
    column_names = [col for col in column_names if col.lower() != 'id']

    # Create table with the remaining columns
    columns_with_types = ', '.join([f"{column} VARCHAR(100) NOT NULL" for column in column_names])
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            {columns_with_types}
        )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Table '{table_name}' created successfully")


def insert_table_data(table_name, csv_file, column_names):
    conn = get_connection()
    if conn is None:
        raise Exception('Database connection is not established.')

    cursor = conn.cursor()

    # Exclude 'id' if it exists in column names
    column_names = [col for col in column_names if col.lower() != 'id']

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = ', '.join(column_names)
        placeholders = ', '.join(['%s'] * len(column_names))

        for row in reader:
            values = [row[col] for col in column_names]
            insert_sql = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """
            cursor.execute(insert_sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data inserted into table '{table_name}' successfully")


def main(table_name, csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        column_names = reader.fieldnames

        create_table(table_name, column_names)
        insert_table_data(table_name, csv_file, column_names)


if __name__ == "__main__":
    # You can change these values to create and insert data into different tables
    table_name = 'cardex_chart'
    csv_file = 'C:/Users/Peter/Blueprint/csv/cardex_chart.csv'
    main(table_name, csv_file)