from flask import Flask
from app.main.routes import main_bp as main_bp  # Assuming main is the blueprint
from app.login.routes import login_bp as login_bp  # Assuming login is another blueprint

def create_app():
    app = Flask(__name__)

    # More descriptive and clear what's being registered
    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)

    return app