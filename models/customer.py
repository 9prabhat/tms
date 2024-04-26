""" models.py file"""

from database import db
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
import re

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    aadhar = db.Column(db.String(15), nullable=False)
    registered_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    plans = db.relationship('CustomerPlan', backref='customer', lazy=True)
    @validates('aadhar')
    def validate_aadhar(self, key, aadhar):
        if not re.match(r'^\d{12}$', aadhar):
            raise ValueError('Invalid aadhar number')
        return aadhar
    @validates('mobile')
    def validate_mobile(self, key, mobile):
        if not re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', mobile):
            raise ValueError('Invalid mobile number')
        return mobile
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Invalid email format')
        return email

class CustomerPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    start_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)