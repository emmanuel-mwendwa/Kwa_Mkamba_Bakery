from . import sales
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required
from .forms import AddNewCustomerForm
from .. import db
from ..models import Customer
from ..decorators import admin_required, permission_required

@sales.route("/")
def sales_page():
    return "Sales Page"

@sales.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    title = "New Customer"
    customer_form = AddNewCustomerForm()
    if customer_form.validate_on_submit():
        new_customer = Customer(
           cust_name = customer_form.cust_name.data,
           cust_email = customer_form.cust_email.data,
           cust_phone_no = customer_form.cust_phone_no.data,
           cust_mpesa_agent_name = customer_form.cust_mpesa_agent_name.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash("Customer added successfully", category="success")
        return "Customer added successfully"
    return render_template("sales/customer/new_customer.html", customer_form=customer_form, title=title)

@sales.route("/view_customers")
def view_customers():
    customers = Customer.query.all()
    return render_template("sales/customer/view_customers.html", customers=customers)

@sales.route("/view_customer/<int:id>")
def view_customer(id):
    return "View Customer"

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
        flash("Customer added successfully", category="success")
        return "Customer editted successfully"
    customer_form.cust_name.data = customer.cust_name
    customer_form.cust_email.data = customer.cust_email
    customer_form.cust_phone_no.data = customer.cust_phone_no
    customer_form.cust_mpesa_agent_name.data = customer.cust_mpesa_agent_name
    return render_template("sales/customer/new_customer.html", customer_form=customer_form, title=title)
