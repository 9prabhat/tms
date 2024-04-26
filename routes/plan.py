from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db
from datetime import datetime, timedelta
import logging
import os
from controllers import plan

plan_blueprint = Blueprint('plan', __name__)


# Add a new plan
@plan_blueprint.route('/add_plan', methods=['POST'])
def add_plan():
    data = request.json
    return plan.add_plan(data)

# Mark plan inactive
@plan_blueprint.route('/mark_plan_inactive/<int:plan_id>', methods=['PUT'])
def mark_plan_inactive(plan_id):
    return plan.mark_plan_inactive(plan_id)

# Get all active plan
@plan_blueprint.route('/get_all_active_plans', methods=['GET'])
def get_all_active_plans():
    return plan.get_all_active_plans()
