from flask import render_template
from flask_login import login_required
from . import main

@main.route('/home')
@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/sales')
@login_required
def sales():
    return render_template('sales.html')

@main.route('/expenses')
@login_required
def expenses():
    return render_template('expenses.html')

@main.route('/staff')
@login_required
def staff():
    return render_template('staff.html')