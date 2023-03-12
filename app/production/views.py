from flask import render_template, redirect, url_for
from flask_login import login_required
from . import production
from .forms import AddProductsForm, AddIngredientsForm, AddProductionRun, AddSupplier, AddInventory
from .. import db
from ..models import Product, Ingredient, ProductionRun, Supplier, Inventory


@production.route('/', methods=["GET", "POST"])
@login_required
def production():
    products = Product.query.all()
    return render_template('production/production.html', products=products)

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


@login_required
def create_ingredient():
    form = AddIngredientsForm()
    if form.validate_on_submit():
        new_ingredient = Ingredient(code=form.code.data, name=form.name.data, unit_cost=form.price.data)
        db.session.add(new_ingredient)
        db.session.commit()
        return redirect(url_for('production.production'))
    return render_template('production/add_ingredient.html', form=form)

# Add new production run 
# @production.route('/add_production_run', methods=["GET", "POST"])
@login_required
def add_production_run():
    form = AddProductionRun()
    if form.validate_on_submit():
        new_production_run = ProductionRun(product_id=form.product_id.data, quantity=form.quantity.data)
        db.session.add(new_production_run)
        db.session.commit()
        return redirect(url_for('production.production'))
    return render_template('production/add_production_run.html', form=form)


@login_required
def add_supplier():
    form = AddSupplier()
    if form.validate_on_submit():
        new_supplier = Supplier(supplier_name=form.name.data, contact_person=form.contact_person.data, contact_number=form.contact_number.data, contact_email=form.contact_email.data, address=form.address.data)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('production.production'))
    return render_template('production/add_supplier.html', form=form)


@login_required
def add_inventory():
    form = AddInventory()
    if form.validate_on_submit():
        new_inventory = Inventory(name=form.product_name.data, current_quantity=form.quantity.data, cost_per_unit=form.cost_per_unit.data)
        db.session.add(new_inventory)
        db.session.commit()
        return redirect(url_for('production.production'))
    return render_template('production/add_inventory.html', form=form)


# View Products 
# @production.route('/view_products', methods=["GET", "POST"])
@login_required
def view_products():
    products = Product.query.all()
    return render_template('production/view_products.html', products=products)