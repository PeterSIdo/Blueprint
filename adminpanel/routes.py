from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from adminpanel.models import AdminUser
from adminpanel.forms import RegistrationForm, LoginForm
from adminpanel.database import db

adminpanel_bp = Blueprint('adminpanel', __name__,template_folder='templates')

@adminpanel_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = AdminUser(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('adminpanel.login'))
    return render_template('register.html', form=form)

@adminpanel_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('adminpanel.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@adminpanel_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('adminpanel.login'))

@adminpanel_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@adminpanel_bp.route('/residents')
@login_required
def residents():
    return render_template('residents.html')