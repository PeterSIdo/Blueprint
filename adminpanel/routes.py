from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from adminpanel.models import AdminUser
from adminpanel.forms import RegistrationForm, LoginForm
from adminpanel.database import db

adminpanel_bp = Blueprint('adminpanel', __name__,template_folder='templates')


@adminpanel_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@adminpanel_bp.route('/residents')
@login_required
def residents():
    return render_template('residents.html')