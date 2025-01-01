from flask import render_template, make_response
from app.auth import auth_bp

from flask import request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from app.db_connection.conn import get_connection
from functools import wraps
from datetime import datetime, timedelta
import time

# Timeout variable for a session 
timeout = 10

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
            session['username'] = user[1]
            
            # Staff access logic
            if user[5] == 'carer':  # Index 5 contains staff_access based on staff_list.txt
                flash('Logged in successfully', 'success')
                return redirect(url_for('carer.carer_menu'))
            
            elif user[5] == 'admin':
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('admin.admin_menu'))
                
            elif user[5] == 'manager':
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('data_input.family_menu'))
                
            elif user[5] == 'family':
                flash('Logged in successfully', 'success')
                return redirect(url_for('family.family_menu'))            
            
            else:
                flash('Logged in successfully', 'success') 
                return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials. Please try again.', 'amber')

    return render_template('auth.html')


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.auth'))
        
        # Check for session timeout
        if 'last_activity' in session:
            last_activity = datetime.fromtimestamp(session['last_activity'])
            if datetime.now() - last_activity > timedelta(minutes=timeout):
                # Session expired
                session.clear()
                flash('Your session has expired. Please log in again.', 'error')
                return redirect(url_for('auth.auth'))
        
        # Update last activity timestamp
        session['last_activity'] = time.time()
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/protected')
@logged_in
def protected_route():
    return 'This is protected content'

# Check staff initials 
@auth_bp.route('/check_staff_initials', methods=['POST'])
def check_staff_initials():
    staff_initials = request.form.get('staff_initials').upper()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if staff_initials exist in staff_list table
    cursor.execute('SELECT 1 FROM staff_list WHERE staff_initials = %s', (staff_initials,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if result is None:
        return jsonify({'valid': False, 'message': 'Invalid staff initials'})
    return jsonify({'valid': True})