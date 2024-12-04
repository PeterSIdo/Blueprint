
from flask import render_template, session
from app.data_input import data_input_bp


@data_input_bp.route('/carer_menu')
def carer_menu():
    return render_template('carer_menu.html')
