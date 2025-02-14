# C:\Users\Peter\Blueprint\app\data_input\input_modules.py
from flask import (
    render_template, redirect, url_for, flash, jsonify, make_response,
    request, session
)
from app.auth import auth_bp
from app.auth.decorators import require_valid_staff_initials
from werkzeug.security import check_password_hash, generate_password_hash
from app.db_connection.conn import get_connection
from functools import wraps
from datetime import datetime, timedelta
import time
from adminpanel.forms import RegistrationForm
from app.db_connection.conn import get_connection  # Make sure you import your database connection helper
from adminpanel.models import StaffList
from adminpanel.forms import RegistrationForm


# Timeout variable for a session 
timeout = 10

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        staff_username = request.form.get('staff_username')
        password = request.form.get('password')

        # Verify that staff_username and password were provided
        if not staff_username or not password:
            flash("Please provide both staff username and password.", 'error')
            return render_template('auth.html')

        # Use the SQLAlchemy ORM to query the user by staff_username
        user = StaffList.query.filter_by(staff_username=staff_username).first()

        # Check if a user exists and the provided password is correct
        if user and check_password_hash(user.password_hash, password):
            session['staff_id'] = user.staff_id
            session['staff_firstname'] = user.staff_firstname
            session['staff_surname'] = user.staff_surname
            session['staff_initials'] = user.staff_initials
            session['staff_email'] = user.staff_email
            session['staff_username'] = user.staff_username
            # Set last activity time so session timeout can be managed.
            session['last_activity'] = time.time()
            flash('Logged in successfully', 'success')


            # Redirect users based on their access level
            if user.staff_access == 'carer':
                return redirect(url_for('carer.carer_menu'))
            elif user.staff_access == 'admin':
                return redirect(url_for('admin.admin_menu'))
            elif user.staff_access == 'manager':
                return redirect(url_for('data_input.family_menu'))
            elif user.staff_access == 'family':
                return redirect(url_for('family.family_menu'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('auth.html')


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Change 'user_id' to 'staff_id' as stored during login.
        if 'staff_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.auth'))
        # Check for session timeout
        if 'last_activity' in session:
            last_activity = datetime.fromtimestamp(session['last_activity'])
            if datetime.now() - last_activity > timedelta(minutes=timeout):
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
        staff_access = form.staff_access.data
        staff_username = form.staff_username.data
        staff_email = form.staff_email.data
        password = form.password.data
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user already exists using staff_email and/or initials
        cursor.execute(
            "SELECT * FROM staff_list WHERE staff_email = %s OR staff_username = %s OR staff_initials =%s", 
            (staff_email, staff_username, staff_initials)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Staff email, username or initials already taken', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.register'))
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Insert new staff into the database
        cursor.execute("""
            INSERT INTO staff_list 
            (staff_firstname, staff_surname, staff_initials, staff_access, staff_email,
            staff_username, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (staff_firstname, staff_surname, staff_initials, staff_access, staff_email, 
                staff_username, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.auth'))
    
    return render_template('register.html', form=form)