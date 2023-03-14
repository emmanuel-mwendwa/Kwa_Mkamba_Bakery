from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from ..models import Product, Supplier


class AddProductsForm(FlaskForm):
    code = StringField('Product Code', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    price = IntegerField('Product Price', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class AddIngredientsForm(FlaskForm):
    code = StringField('Ingredient Code', validators=[DataRequired()])
    name = StringField('Ingredient Name', validators=[DataRequired()])
    price = IntegerField('Ingredient Price', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[])
    submit = SubmitField('Add Ingredient')


class AddProductionRun(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    quantity = IntegerField('Packets Produced', validators=[DataRequired()])
    submit = SubmitField('Add Production Run')

    def __init__(self, *args, **kwargs):
        super(AddProductionRun, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name)
                                   for product in Product.query.order_by(Product.name).all()]


class AddSupplier(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    contact_number = IntegerField('Contact Integer', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired()])
    address = StringField('Address')
    submit = SubmitField('Add Supplier')


class AddInventory(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    cost_per_unit = IntegerField('Cost per Unit', validators=[DataRequired()])
    submit = SubmitField('Add Inventory')