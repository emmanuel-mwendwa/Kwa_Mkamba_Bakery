from flask import render_template, redirect, url_for, flash, request
from . import production
from .forms import AddNewProductForm, AddNewProductionRunForm, EditProductForm, EditProductionRunForm
from .. import db
from ..models import Product, ProductionRun
from ..decorators import admin_required

# Add a new product in the database
@production.route('/new_product', methods=["GET", "POST"])
@admin_required
def new_product():
    form = AddNewProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, description=form.description.data)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully", category="success")
        return redirect(url_for("production.view_products"))
    return render_template("production/new_items.html", form=form)

# View the products in the database
@production.route('/view_products', methods=["GET", "POST"])
def view_products():
    products = Product.query.all()
    return render_template("production/view_products.html", products=products)

# Edit values of the products in the database
@production.route('/product/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = EditProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        db.session.add(product)
        db.session.commit()
        flash("Product Updated Successfully", category="success")
        return redirect(url_for("production.view_products"))
    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    return render_template("production/edit_product.html", form=form)

# Delete products in the database
@production.route('/product_delete/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("production.view_products"))

# New production run
@production.route('/new_productionrun', methods=["GET", "POST"])
@admin_required 
def new_productionrun():
    form = AddNewProductionRunForm()
    if form.validate_on_submit():
        new_productionrun = ProductionRun(product_id=form.product_id.data, quantity=form.quantity.data, flour_kneaded=form.flour_kneaded.data, oil_used=form.oil_used.data)
        db.session.add(new_productionrun)
        db.session.commit()
        flash("Production run added successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    return render_template("production/new_items.html", form=form)

# View production runs
@production.route('/view_productionruns', methods=["GET", "POST"])
def view_productionruns():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    query = db.session.query(ProductionRun, Product.name).join(Product, ProductionRun.product_id == Product.id).order_by(ProductionRun.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page)
    productionruns = pagination.items
    return render_template("production/view_productionruns.html", productionruns=productionruns, pagination=pagination)

# Edit production runs
@production.route('/productionrun/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_productionrun(id):
    productionrun = ProductionRun.query.get_or_404(id)
    form = EditProductionRunForm()
    if form.validate_on_submit():
        productionrun.product_id = form.product_id.data
        productionrun.quantity = form.quantity.data
        productionrun.flour_kneaded = form.flour_kneaded.data
        productionrun.oil_used = form.oil_used.data
        db.session.add(productionrun)
        db.session.commit()
        flash("Production run edited successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    form.product_id.data = productionrun.product_id
    form.quantity.data = productionrun.quantity
    form.flour_kneaded.data = productionrun.flour_kneaded
    form.oil_used.data = productionrun.oil_used
    return render_template("production/edit_productionrun.html", form=form)

# Delete products in the database
@production.route('/productionrun_delete/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_productionrun(id):
    productionrun = ProductionRun.query.get_or_404(id)
    db.session.delete(productionrun)
    db.session.commit()
    return redirect(url_for("production.view_productionruns"))