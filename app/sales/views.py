from . import sales
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required
from .forms import AddNewCustomerForm, AddNewRouteForm, DispatchForm, OrderForm
from .. import db
from ..models import Customer, Route, User, Dispatch, DispatchDetails, Order, OrderDetail
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

@sales.route("/update_route/<int:id>", methods=["GET", "POST"])
def update_route(id):
    title = "Update Route"
    route = Route.query.get_or_404(id)
    route_form = AddNewRouteForm()
    if route_form.validate_on_submit():
        route.route_name = route_form.route_name.data
        route.sales_assoc_id = route_form.sales_assoc_id.data

        db.session.add(route)
        db.session.commit()
        flash("Route updated successfully", category="success")
        return redirect(url_for("sales.view_route", id=route.route_id))
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

@sales.route("/update_customer/<int:id>", methods=["GET", "POST"])
def update_customer(id):
    title = "Update Customer"
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
    return render_template("sales/dispatch/new_dispatch.html", dispatch_form=dispatch_form, title=title)


@sales.route("/view_dispatches")
def view_dispatches():
    dispatches = Dispatch.query.all()
    return render_template("sales/dispatch/view_dispatches.html", dispatches=dispatches)

@sales.route("/view_dispatch/<int:id>")
def view_dispatch(id):
    dispatch = Dispatch.query.get_or_404(id)
    return render_template("sales/dispatch/view_dispatch.html", dispatch=dispatch)

@sales.route("/edit_dispatch/<int:id>", methods=["GET", "POST"])
def update_dispatch(id):
    title = "Update Dispatch"
    dispatch = Dispatch.query.get(id)
    if dispatch is None:
        # Handle case where dispatch is not found
        return "Dispatch not found", 404

    # populates the form fields with data fetched from dispatch query
    dispatch_form = DispatchForm(obj=dispatch)

    if dispatch_form.validate_on_submit():
        dispatch_form.populate_obj(dispatch)
          # Update dispatch data
        dispatch.dispatch_date = datetime.utcnow()
        dispatch.route_id = dispatch_form.route_id.data

        # Update dispatch details
        for index, dispatch_details_form in enumerate(dispatch_form.dispatch_details):
            dispatch_details = dispatch.dispatch_details[index]
            if dispatch_details_form and dispatch_details_form.product_id.data != 0:
                dispatch_details.product_id = dispatch_details_form.product_id.data
                dispatch_details.quantity = dispatch_details_form.quantity.data
                dispatch_details.returns = dispatch_details_form.returns.data

        db.session.commit()
        return redirect(url_for("sales.view_dispatch", id=dispatch.dispatch_id))

    return render_template("sales/dispatch/new_dispatch.html", dispatch_form=dispatch_form, title=title)

@sales.route('/delete_dispatch/<int:id>', methods=["GET", "POST"])
def delete_dispatch(id):
    dispatch = Dispatch.query.get_or_404(id)

    # Delete corresponding dispatch details
    for dispatch_detail in dispatch.dispatch_details:
        db.session.delete(dispatch_detail)

    db.session.delete(dispatch)
    db.session.commit()
    return redirect(url_for("sales.view_dispatches"))

@sales.route('/new_order', methods=["GET", "POST"])
def new_order():
    title = "New Order"
    order_form = OrderForm()
    if order_form.validate_on_submit():
        if 'add_order' in request.form:
            order_form.add_empty_orderdetail()
        elif 'submit_order' in request.form:
            order = Order(
                order_date = datetime.utcnow(),
                order_notes = order_form.order_notes.data,
                customer_id = order_form.customer_id.data,
                payment_method_id = order_form.payment_method_id.data
            )
            db.session.add(order)
            db.session.commit()

            for order_details_form in order_form.order_details:
                if order_details_form.product_id.data != 0:
                    order_detail = OrderDetail(
                        order_id = order.order_id,
                        product_id = order_details_form.product_id.data,
                        quantity = order_details_form.quantity.data
                    )
                    db.session.add(order_detail)
            db.session.commit()
            return redirect(url_for("sales.view_orders"))
    return render_template("sales/orders/new_order.html", order_form=order_form, title=title)

@sales.route('/view_orders')
def view_orders():
    orders = Order.query.all()
    return render_template("sales/orders/view_orders.html", orders=orders)

@sales.route('/view_order/<int:order_id>')
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("sales/orders/view_order.html", order=order)

@sales.route('/update_order/<int:order_id>', methods=["GET", "POST"])
def update_order(order_id):
    title = "Update Order"
    order = Order.query.get(order_id)
    if order is None:
        # Handle case where order is not found
        return "Order not found", 404

    # populates the form fields with data fetched from order query
    order_form = OrderForm(obj=order)

    if order_form.validate_on_submit():
        order_form.populate_obj(order)
          # Update order data
        order.order_date = datetime.utcnow()
        order.customer_id = order_form.customer_id.data
        order.notes = order_form.order_notes.data
        order.payment_method_id = order_form.payment_method_id.data

        # Update order details
        for index, order_details_form in enumerate(order_form.order_details):
            order_details = order.order_details[index]
            if order_details_form and order_details_form.product_id.data != 0:
                order_details.product_id = order_details_form.product_id.data
                order_details.quantity = order_details_form.quantity.data

        db.session.commit()
        return redirect(url_for("sales.view_order", order_id=order.order_id))
    return render_template("sales/orders/new_order.html", order_form=order_form, title=title)

@sales.route('/delete_order/<int:order_id>', methods=["GET", "POST"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Delete corresponding order details
    for order_detail in order.order_details:
        db.session.delete(order_detail)

    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("sales.view_orders"))