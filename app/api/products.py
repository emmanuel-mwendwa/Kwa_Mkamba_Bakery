from flask import jsonify, request
from . import api
from .. import db
from app.models import Product
import json

class Products_Routes():
    @api.post("/new_product")
    def new_product():
        data = request.get_json()
        # product = Product(
        #     name=data["name"],
        #     price=data["price"],
        #     description=data["description"]
        # )
        # db.session.add(product)
        # db.session.commit()
        name = data["name"]
        price= data["price"]
        desc = data["description"]
        return jsonify({"message": [
            {"name": name,
             "price": price,
             "desc": desc
            }
        ]})

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