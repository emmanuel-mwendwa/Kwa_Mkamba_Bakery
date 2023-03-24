from flask import render_template, redirect, url_for, flash
from . import production
from .forms import AddNewProductForm
from .. import db
from ..models import Product

@production.route('/new_product', methods=["GET", "POST"])
def new_product():
    form = AddNewProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, description=form.description.data)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully", category="success")
        return redirect(url_for("production.view_products"))
    return render_template("production/new_items.html", form=form)


@production.route('/view_products', methods=["GET", "POST"])
def view_products():
    products = Product.query.all()
    return render_template("production/view.html", products=products)

