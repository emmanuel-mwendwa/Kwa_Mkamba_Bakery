from . import sales

@sales.route("/")
def sales_page():
    return "Sales Page"

@sales.route("/new_customer")
def new_customer():
    return "Add Customer"

@sales.route("/view_customers")
def view_customers():
    return "View Customers"

@sales.route("/view_customer/<int:id>")
def view_customer(id):
    return "View Customer"

@sales.route("/edit_customer")
def edit_customer():
    return "Edit Customer"
