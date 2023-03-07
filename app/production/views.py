from flask import render_template, redirect, url_for
from flask_login import login_required
from . import production
from .forms import AddProductsForm
from .. import db
from ..models import Product


@production.route('/', methods=["GET", "POST"])
@login_required
def production():
    return render_template('production/production.html')

# Add new products to the database
# @production.route('/create_product', methods=["GET", "POST"])
@login_required
def create_product():
    form = AddProductsForm()
    if form.validate_on_submit():
        new_product = Product(code=form.code.data, name=form.name.data, description=form.description.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('production.production'))
    return render_template('production/add_product.html', form=form)

# Add new production run 
# @production.route('/add_production_run', methods=["GET", "POST"])
@login_required
def add_production_run():
    return render_template('production/add_production_run.html')

# View Products 
# @production.route('/view_products', methods=["GET", "POST"])
@login_required
def view_products():
    products = Product.query.all()
    return render_template('production/view_products.html', products=products)