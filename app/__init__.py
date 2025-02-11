import sys
from os.path import abspath, dirname
# Add 'app' directory to the sys.path
sys.path.append(dirname(abspath(__file__)) + '/app')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.main.routes import main_bp as main_bp 
from app.login.routes import login_bp as login_bp 
from app.auth.routes import auth_bp as auth_bp
from app.db_connection import db_connection_bp as db_connection_bp
from app.data_input.routes import data_input_bp as data_input_bp
from app.data_output.routes import data_output_bp as data_output_bp
#from app.admin.routes import admin_bp as admin_bp
from app.carer.routes import carer_bp as carer_bp
from app.staff_board.routes import staff_board_bp as staff_board_bp

from adminpanel.routes import adminpanel_bp
from adminpanel.models import AdminUser
from app.db_connection.config import Config

db = SQLAlchemy()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config.from_object('adminpanel.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_db_uri()   
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'adminpanel.login'  # Redirect to adminpanel.login if user not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # More descriptive and clear what's being registered
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(db_connection_bp)
    app.register_blueprint(data_input_bp)
    app.register_blueprint(data_output_bp)
    #app.register_blueprint(admin_bp)
    app.register_blueprint(carer_bp)
    app.register_blueprint(staff_board_bp)
    app.register_blueprint(adminpanel_bp)

    return app