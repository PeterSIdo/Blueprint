from functools import wraps
from flask import request, flash, redirect, url_for
from app.db_connection.conn import get_connection

def require_valid_staff_initials(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        staff_initials = request.form.get('staff_initials')
        if not staff_initials:
            flash('Staff initials are required.', 'error')
            return redirect(url_for('data_input.food_intake'))
            
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1 FROM staff_list WHERE staff_initials = %s', 
                         (staff_initials.upper(),))
            if cursor.fetchone() is None:
                flash('Invalid staff initials.', 'error')
                return redirect(url_for('data_input.food_intake'))
        conn.close()
        return f(*args, **kwargs)
    return decorated_function