
from flask import render_template, session
from app.admin import admin_bp


@admin_bp.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')