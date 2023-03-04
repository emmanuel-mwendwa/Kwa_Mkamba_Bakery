from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main
from .forms import AddProductsForm
from .. import db
from ..models import Product

@main.route('/home')
@main.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Add new products to the database
@main.route('/production', methods=["GET", "POST"])
@login_required
def production():
    form = AddProductsForm()
    if form.validate_on_submit():
        new_product = Product(code=form.code.data, name=form.name.data, description=form.description.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('production.html', form=form)


@main.route('/production/daily', methods=["GET", "POST"])
@login_required
def production():
    pass


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