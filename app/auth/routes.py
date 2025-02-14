# C:\Users\Peter\Blueprint\app\data_input\input_modules.py
from flask import render_template, redirect, url_for, flash, jsonify, make_response
from app.auth import auth_bp
from app.auth.decorators import require_valid_staff_initials

from flask import request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.db_connection.conn import get_connection
from functools import wraps
from datetime import datetime, timedelta
import time
from adminpanel.forms import RegistrationForm
from app.db_connection.conn import get_connection  # Make sure you import your database connection helper


# Timeout variable for a session 
timeout = 10

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Get the staff_username and password from the form
        staff_username = request.form.get('staff_username')
        password = request.form.get('password')
        
        conn = get_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return render_template('auth.html')
        
        cursor = conn.cursor()
        # Look up the user by staff_username
        cursor.execute("SELECT * FROM staff_list WHERE staff_username = %s", (staff_username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Check if user exists and the password matches the generated hash
        if user and check_password_hash(user[7], password):
            session['user_id'] = user[0]
            session['staff_firstname'] = user[1]  # Using staff_username for the session
            
            # Redirect based on user's access level (staff_access is index 4)
            if user[4] == 'carer':
                flash('Logged in successfully', 'success')
                return redirect(url_for('carer.carer_menu'))
            elif user[4] == 'admin':
                flash('Logged in successfully', 'success')
                return redirect(url_for('admin.admin_menu'))
            elif user[4] == 'manager':
                flash('Logged in successfully', 'success')
                return redirect(url_for('data_input.family_menu'))
            elif user[4] == 'family':
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

def validate_staff_initials(staff_initials):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT 1 FROM staff_list WHERE staff_initials = %s', (staff_initials,))
        result = cursor.fetchone()
        conn.close()
        return result is not None


# Require valid staff initials
def require_valid_staff_initials(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        staff_initials = request.form.get('staff_initials')
        if not validate_staff_initials(staff_initials):
            flash('Invalid staff initials. Please check and try again.', 'amber')
            return redirect(url_for('data_input.collect_data'))
        return f(*args, **kwargs)
    return decorated_function


# Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Extract data from form fields
        staff_firstname = form.staff_firstname.data
        staff_surname = form.staff_surname.data
        staff_initials = form.staff_initials.data
        staff_username = form.staff_username.data  # New field
        staff_email = form.staff_email.data
        staff_access = form.staff_access.data
        password = form.password.data

        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user already exists based on email, initials or username
        cursor.execute(
            "SELECT * FROM staff_list WHERE staff_email = %s OR staff_initials = %s OR staff_username = %s", 
            (staff_email, staff_initials, staff_username)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Staff email, initials, or username already taken', 'error')
            return redirect(url_for('auth.register'))
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Insert new staff into the database including staff_username field
        cursor.execute("""
            INSERT INTO staff_list 
            (staff_firstname, staff_surname, staff_initials, staff_username, staff_access, staff_email, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (staff_firstname, staff_surname, staff_initials, staff_username, staff_access, staff_email, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.auth'))
    return render_template('register.html', form=form)