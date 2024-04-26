from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db
from datetime import datetime, timedelta
import logging
import os
from models.plan import *


def add_plan(data):
    try:
        new_plan = Plan(name=data['name'], cost=data['cost'], validity=data['validity'], status=data['status'])
        db.session.add(new_plan)
        db.session.commit()
        return jsonify({'message': 'Plan added successfully', 'plan': data}), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

def mark_plan_inactive(plan_id):
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'message': 'Plan not found'}), 404
        # Mark the plan as inactive
        plan.status = 'Inactive'
        db.session.commit()
        return jsonify({'message': 'Plan marked as inactive successfully'}), 200
    except Exception as e:
        return jsonify({"errors": str(e)}), 400


def get_all_active_plans():
    try:
        active_plans = Plan.query.filter_by(status='Active').all()
        plans = []
        for plan in active_plans:
            plan_data = {
                'id': plan.id,
                'name': plan.name,
                'cost': plan.cost,
                'validity': plan.validity,
                'status': plan.status
            }
            plans.append(plan_data)
        return jsonify({'active_plans': plans})
    except Exception as e:
        return jsonify({"errors": str(e)}), 400