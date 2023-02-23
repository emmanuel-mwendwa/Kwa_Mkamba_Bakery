from flask import render_template
from . import main

@main.route('/home')
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/products')
def products():
    return render_template('products.html')

@main.route('/stocks')
def stocks():
    return render_template('stocks.html')

@main.route('/sales')
def sales():
    return render_template('sales.html')

@main.route('/point_of_sale')
def point_of_sale():
    return render_template('point_of_sale.html')