from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db
from datetime import datetime, timedelta
import logging
import os
from config import *
from routes.customer import customer_blueprint
from routes.plan import plan_blueprint

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    print(env)
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()

app = Flask(__name__)
app.config.from_object(get_config())

db.init_app(app)

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    from models import *
    create_db()
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(plan_blueprint)
    app.run(host="0.0.0.0")