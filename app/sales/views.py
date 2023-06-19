from . import sales

@sales.route("/")
def sales():
    return "Sales Page"