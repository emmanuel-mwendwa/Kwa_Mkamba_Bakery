from flask import jsonify
from . import api
from app.models import Product
import json

@api.get("/view_products")
def view_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_list.append(product.to_json())

    return jsonify(products_list)

@api.get("/view_product/<int:id>")
def view_product(id):
    product = Product.query.get_or_404(id)
    production_runs = product.production_runs.all()
    product = product.to_json()
    runs = []
    for production_run in production_runs:
        runs.append(production_run.to_json())

    return jsonify([product, runs])