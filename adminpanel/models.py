from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from adminpanel.database import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StaffList(db.Model):
    __tablename__ = 'staff_list'
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_firstname = db.Column(db.String(50), nullable=False)
    staff_surname = db.Column(db.String(50), nullable=False)
    staff_initials = db.Column(db.String(10), nullable=False)
    staff_access = db.Column(db.String(20), nullable=False)
    staff_email = db.Column(db.String(50), nullable=False)
    staff_username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<StaffList {self.staff_email}>"
  