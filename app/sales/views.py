from . import sales
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required
from .forms import AddNewCustomerForm, AddNewRouteForm, DispatchForm
from .. import db
from ..models import Customer, Route, User, Dispatch, DispatchDetails
from ..decorators import admin_required, permission_required
from datetime import datetime

@sales.route("/")
def sales_page():
    return render_template("sales/sales.html")

@sales.route("/new_route", methods=["GET", "POST"])
def new_route():
    title = "New Route"
    route_form = AddNewRouteForm()
    if route_form.validate_on_submit():
        new_route = Route(
            route_name = route_form.route_name.data,
            sales_assoc_id = route_form.sales_assoc_id.data
        )
        db.session.add(new_route)
        db.session.commit()
        return redirect(url_for('sales.view_route', id=new_route.route_id))
    return render_template("sales/route/new_route.html", route_form=route_form, title=title)

@sales.route("/view_routes")
def view_routes():
    routes = Route.query.all()
    return render_template("sales/route/view_routes.html", routes=routes)

@sales.route("/view_route/<int:id>")
def view_route(id):
    route = Route.query.get_or_404(id)
    sales_assoc = User.query.filter_by(id = route.sales_assoc_id).first()
    return render_template("sales/route/view_route.html", route=route, sales_assoc=sales_assoc)

@sales.route("/edit_route/<int:id>", methods=["GET", "POST"])
def edit_route(id):
    title = "Edit Route"
    route = Route.query.get_or_404(id)
    route_form = AddNewRouteForm()
    if route_form.validate_on_submit():
        route.route_name = route_form.route_name.data
        route.sales_assoc_id = route_form.sales_assoc_id.data

        db.session.add(route)
        db.session.commit()
        flash("Route editted successfully", category="success")
        return "Route editted successfully"
    route_form.route_name.data = route.route_name
    route_form.sales_assoc_id.data = route.sales_assoc_id
    return render_template("sales/route/new_route.html", route_form=route_form, title=title)

@sales.route('/delete_route/<int:id>', methods=["GET", "POST"])
def delete_route(id):
    route = Route.query.get_or_404(id)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for("sales.view_routes"))

@sales.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    title = "New Customer"
    customer_form = AddNewCustomerForm()
    if customer_form.validate_on_submit():
        new_customer = Customer(
           cust_name = customer_form.cust_name.data,
           cust_email = customer_form.cust_email.data,
           cust_phone_no = customer_form.cust_phone_no.data,
           cust_mpesa_agent_name = customer_form.cust_mpesa_agent_name.data,
           route_id = customer_form.route_id.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash("Customer added successfully", category="success")
        return redirect(url_for('sales.view_customer', id=new_customer.cust_id))
    return render_template("sales/customer/new_customer.html", customer_form=customer_form, title=title)

@sales.route("/view_customers")
def view_customers():
    customers = Customer.query.all()
    return render_template("sales/customer/view_customers.html", customers=customers)

@sales.route("/view_customer/<int:id>")
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template("sales/customer/view_customer.html", customer=customer)

@sales.route("/edit_customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):
    title = "Edit Customer"
    customer = Customer.query.get_or_404(id)
    customer_form = AddNewCustomerForm()
    if customer_form.validate_on_submit():
        customer.cust_name = customer_form.cust_name.data
        customer.cust_email = customer_form.cust_email.data
        customer.cust_phone_no = customer_form.cust_phone_no.data
        customer.cust_mpesa_agent_name = customer_form.cust_mpesa_agent_name.data

        db.session.add(customer)
        db.session.commit()
        flash("Customer editted successfully", category="success")
        return redirect(url_for('sales.view_customer', id=customer.cust_id))
    customer_form.cust_name.data = customer.cust_name
    customer_form.cust_email.data = customer.cust_email
    customer_form.cust_phone_no.data = customer.cust_phone_no
    customer_form.cust_mpesa_agent_name.data = customer.cust_mpesa_agent_name
    return render_template("sales/customer/new_customer.html", customer_form=customer_form, title=title)

@sales.route('/delete_customer/<int:id>', methods=["GET", "POST"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for("sales.view_customers"))

@sales.route('/new_dispatch', methods=["GET", "POST"])
def new_dispatch():
    title = "New Dispatch"
    dispatch_form = DispatchForm()
    if dispatch_form.validate_on_submit():
        if 'add_dispatch' in request.form:
            dispatch_form.add_empty_dispatch()
        elif 'submit_dispatch' in request.form:
            dispatch = Dispatch(
                dispatch_date = datetime.utcnow(),
                route_id = dispatch_form.route_id.data
            )
            db.session.add(dispatch)
            db.session.commit()

            for dispatch_details_form in dispatch_form.dispatch_details:
                if dispatch_details_form.product_id.data != 0:
                    dispatch_detail = DispatchDetails(
                        dispatch_id = dispatch.dispatch_id,
                        product_id = dispatch_details_form.product_id.data,
                        quantity = dispatch_details_form.quantity.data,
                        returns = dispatch_details_form.returns.data
                    )
                    db.session.add(dispatch_detail)
            db.session.commit()
            return redirect(url_for("sales.view_dispatches"))
    return render_template("sales/dispatch/new_dispatch.html", dispatch_form=dispatch_form)


@sales.route("/view_dispatches")
def view_dispatches():
    dispatches = Dispatch.query.all()
    return render_template("sales/dispatch/view_dispatches.html", dispatches=dispatches)

def get_user_details_by_route_id(route_id):
    # Join Dispatch and Route tables on route_id
    dispatch_query = db.session.query(Dispatch).filter_by(route_id=route_id).subquery()
    join_query = db.session.query(User).join(Route, User.sales_assoc).join(dispatch_query, Route.dispatch_route).all()

    return join_query

@sales.route("/view_dispatch/<int:id>")
def view_dispatch(id):
    pass