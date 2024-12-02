import sys
from os.path import abspath, dirname
# Add 'app' directory to the sys.path
sys.path.append(dirname(abspath(__file__)) + '/app')

from flask import Flask
from app.main.routes import main_bp as main_bp 
from app.login.routes import login_bp as login_bp 
from app.auth.routes import auth_bp as auth_bp
from app.db_connection import db_connection_bp as db_connection_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # More descriptive and clear what's being registered
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(db_connection_bp)    

    return app