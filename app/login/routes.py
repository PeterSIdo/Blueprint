from flask import render_template
from app.login import login_bp

@login_bp.route('/login')
def login():
    return render_template('login.html')

@login_bp.route('/register')
def register():
    return render_template('register.html')

@login_bp.route('/logout')
def logout():
    return render_template('logout.html')