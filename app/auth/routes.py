from flask import render_template, make_response
from app.auth import auth_bp

from flask import request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from app.db_connection.conn import get_connection

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():

    if request.method == 'POST':
        staff_unique_id = request.form.get('staff_unique_id')
        password = request.form.get('password')

        conn = get_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return render_template('auth.html')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff_list WHERE staff_unique_id = %s", (staff_unique_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[7], password):
            session['user_id'] = user[0]
            session['username'] = f"{user[1]} {user[2]}"
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'amber')

    return render_template('auth.html')

@auth_bp.route('/access')
def access():
    conn = get_connection()
    if conn is None:
        return "Database connection failed", 500
    else:
        conn.close()
        return "Database connection successful", 200