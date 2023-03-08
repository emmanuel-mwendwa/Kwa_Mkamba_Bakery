from flask import Blueprint

production = Blueprint('production', __name__)

from . import views


production.add_url_rule(
    "/create_product",
    view_func=views.create_product,
    methods=["GET", "POST"]
)

production.add_url_rule(
    "/create_ingredient",
    view_func=views.create_ingredient,
    methods=["GET", "POST"]
)

production.add_url_rule(
    "/add_supplier",
    view_func=views.add_supplier,
    methods=["GET", "POST"]
)

production.add_url_rule(
    "/add_inventory",
    view_func=views.add_inventory,
    methods=["GET", "POST"]
)


production.add_url_rule(
    "/add_production_run",
    view_func=views.add_production_run,
    methods=["GET", "POST"]
)

production.add_url_rule(
    "/view_products",
    view_func=views.view_products,
    methods=["GET", "POST"]
)