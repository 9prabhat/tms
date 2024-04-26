from flask import Blueprint
from templates import *
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db
from datetime import datetime, timedelta
import logging
import os
from models.customer import *
from controllers import customer


customer_blueprint = Blueprint('customer', __name__)

# Add new customer
@customer_blueprint.route('/add_customer', methods=['POST'])
def add_customer():
    return customer.add_customer(request.json)

# Get all customers with their active plan
@customer_blueprint.route('/get_all_customers', methods=['GET'])
def get_customers_with_active_plan_dates():
    return customer.get_customers_with_active_plan_dates()

# Update customer plan (Renew plan, Upate a new plan, upgrade or downgrade to any plan)
@customer_blueprint.route('/update_customer_plan/<int:customer_id>', methods=['PUT'])
def update_customer_plan(customer_id):
    return customer.update_customer_plan(customer_id)

# Home Page
@customer_blueprint.route('/', methods=['GET'])
def get_customers_with_active_plan_dates_html():
    data = customer.get_customers_with_active_plans()
    return render_template('home.html', customers_with_plans=data)

