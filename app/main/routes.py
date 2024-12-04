from flask import render_template
from app.main import main_bp

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/logout')
def logout():
    return render_template('logout.html')