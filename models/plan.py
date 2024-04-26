""" models.py file"""

from database import db
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
import re
from models.customer import *

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cost = db.Column(db.Integer)
    validity = db.Column(db.Integer)
    status = db.Column(db.Enum('Active', 'Inactive', name='plan_status'))
    customers = db.relationship('CustomerPlan', backref='plan', lazy=True)
    __table_args__ = (
        db.UniqueConstraint('cost', 'validity', name='unique_cost_validity'),
    )