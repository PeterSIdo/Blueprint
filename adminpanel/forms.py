from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    staff_firstname = StringField('First Name', validators=[DataRequired()])
    staff_surname = StringField('Surname', validators=[DataRequired()])
    staff_initials = StringField('Initials', validators=[DataRequired(), Length(max=5)])
    staff_unique_id = StringField('Unique ID', validators=[DataRequired()])
    staff_access = StringField('Access Level', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')