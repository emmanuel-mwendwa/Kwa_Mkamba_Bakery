from flask import render_template, redirect, url_for, flash, request
from . import production
from .forms import AddNewProductForm, AddNewProductionRunForm
from .. import db
from ..models import Product, Production_Run
from ..decorators import admin_required

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

@production.route('/new_productionrun', methods=["GET", "POST"])
@admin_required
def new_productionrun():
    form = AddNewProductionRunForm()
    if form.validate_on_submit():
        new_productionrun = Production_Run(product_id=form.product_id.data, quantity=form.quantity.data, flour_kneaded=form.flour_kneaded.data )
        db.session.add(new_productionrun)
        db.session.commit()
        flash("Production run added successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    return render_template("production/new_items.html", form=form)


@production.route('/view_products', methods=["GET", "POST"])
def view_products():
    products = Product.query.all()
    return render_template("production/view.html", products=products)

@production.route('/view_productionruns', methods=["GET", "POST"])
def view_productionruns():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    query = db.session.query(Production_Run, Product.name).join(Product, Production_Run.product_id == Product.id).order_by(Production_Run.date_created.desc())
    pagination = query.paginate(page=page, per_page=per_page)
    productionruns = pagination.items
    return render_template("production/productionruns.html", productionruns=productionruns, pagination=pagination)

