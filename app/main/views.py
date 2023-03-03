from flask import render_template
from . import main

@main.route('/home')
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/production')
def production():
    return render_template('production.html')

@main.route('/sales')
def sales():
    return render_template('sales.html')

@main.route('/expenses')
def expenses():
    return render_template('expenses.html')

@main.route('/staff')
def staff():
    return render_template('staff.html')