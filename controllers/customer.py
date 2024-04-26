from database import db
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import logging
from models.customer import *
from models.plan import *
from utils.helpers import *

def add_customer(data):
    try:
        customer = Customer(name=data['name'],
                            mobile=data['mobile'],
                            dob=datetime.strptime(data['dob'], '%d-%m-%Y').date(),
                            email=data['email'],
                            aadhar=data['aadhar'])
        db.session.add(customer)
        plan = Plan.query.get(data['plan_id'])
        start_date = datetime.utcnow()
        customer_plan = CustomerPlan(plan=plan, start_date=start_date, expiry_date=get_expiry_date(plan.validity))
        customer.plans.append(customer_plan)
        db.session.commit()
        return jsonify({'message': 'Customer added successfully', 'customer': data}), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400 


def get_customers_with_active_plan_dates():
    try:
        customers_with_active_plans = []
        all_customers = Customer.query.all()
        for customer in all_customers:
            plan = customer.plans[0]
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'mobile': customer.mobile,
                'aadhar': customer.aadhar,
                'registration_date': str(customer.registered_at),
                'plan_name': plan.plan.name,
                'plan_start_date': str(plan.start_date),
                'plan_expiry_date': str(plan.expiry_date)
            }
            customers_with_active_plans.append(customer_data)
        return jsonify({'customers_with_active_plans': customers_with_active_plans})
    except Exception as e:
        return jsonify({"errors": str(e)}), 400


def update_customer_plan(customer_id):
    try:
        data = request.json
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        plan_id = data.get('plan_id')
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'message': 'Plan not found'}), 404
        
        current_customer_plan = CustomerPlan.query.filter_by(customer_id=customer_id).first()
        if current_customer_plan:
            db.session.delete(current_customer_plan)

        start_date = datetime.utcnow()
        customer_plan = CustomerPlan(plan=plan, start_date=start_date, expiry_date=get_expiry_date(plan.validity))
        customer.plans.append(customer_plan)
        db.session.commit()
        return jsonify({'message': 'Customer plan updated successfully'}), 200
    except Exception as e:
        return jsonify({"errors": str(e)}), 400


def get_customers_with_active_plans():
    try:
        customers_with_active_plans = []
        all_customers = Customer.query.all()
        for customer in all_customers:
            plan = customer.plans[0]
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'mobile': customer.mobile,
                'aadhar': customer.aadhar,
                'registration_date': str(customer.registered_at),
                'plan_name': plan.plan.name,
                'plan_start_date': str(plan.start_date),
                'plan_expiry_date': str(plan.expiry_date)
            }
            customers_with_active_plans.append(customer_data)
        return customers_with_active_plans
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
