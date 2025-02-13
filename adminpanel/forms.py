from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    staff_firstname = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    staff_surname = StringField('Surname', validators=[DataRequired(), Length(max=50)])
    staff_initials = StringField('Initials', validators=[DataRequired(), Length(max=10)])
    staff_access = StringField('Access Level', validators=[DataRequired(), Length(max=20)])
    staff_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    # Password will be hashed later; we use a PasswordField to capture the user's input
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')