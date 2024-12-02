# app/login/auth.py
import sys
from os.path import abspath, dirname

# Add 'app' directory to the sys.path
#sys.path.append(dirname(abspath(__file__)) + '/app')
sys.path.append(dirname(dirname(abspath(__file__))))

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from app.db_connection.conn import get_connection
from app.auth import auth_bp


"""
The provided code defines Flask routes for user login and logout functionality with password hashing
and session management.
:return: The code provided defines a Flask Blueprint named 'auth' with routes for login and logout
functionalities.

import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

"""

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        staff_unique_id = request.form.get('staff_unique_id')
        print(staff_unique_id)
        password = request.form.get('password')

        conn = get_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return render_template('login.html')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff_list WHERE staff_unique_id = %s", (staff_unique_id,))
        print (staff_unique_id)
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[7], password):  
            session['user_id'] = user[0]
            session['username'] = f"{user[1]} {user[2]}"  # Assuming first and last name are 2nd and 3rd columns
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('auth.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.index'))