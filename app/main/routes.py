from flask import render_template, session
from app.main import main_bp
from app.db_connection.conn import get_connection

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@main_bp.route('/access')
def access():
    conn = get_connection()
    if conn is None:
        return "Database connection failed", 500
    else:
        conn.close()
        return "Database connection successful", 200
