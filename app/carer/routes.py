
from flask import render_template, session
from app.carer import carer_bp


@carer_bp.route('/carer_menu')
def carer_menu():
    return render_template('carer_menu.html')
