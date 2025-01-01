# C:\Users\Peter\Blueprint\app\carer\routes.py
from flask import render_template, session
from app.carer import carer_bp
from app.auth.routes import logged_in

@carer_bp.route('/carer_menu')
@logged_in
def carer_menu():
    return render_template('carer_menu.html')

