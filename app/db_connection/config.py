# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_NAME = os.environ.get('DB_NAME', 'care6')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'jelszo')
    
    DB_HOST = os.environ.get('DB_HOST', '34.105.189.70') # External IP access
    #DB_HOST = os.environ.get('DB_HOST', '172.24.250.3') # Internal Google access
    
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_MIN_CONNECTIONS = 1
    DB_MAX_CONNECTIONS = 20

    @staticmethod
    def get_db_uri():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"