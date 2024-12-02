# db_connection/conn.py
import psycopg2
from app.db_connection.config import Config


def get_connection():
    try:
        connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        return connection
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None


def init_db_connection(app):
    app.config['db_connection'] = get_connection()