from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from ..models import Product, ProductionRun

class AddNewProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Add")


class EditProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Edit")


class AddNewProductionRunForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    flour_kneaded = IntegerField('Flour Kneaded')
    oil_used = IntegerField('Oil used')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Add')

    # adding choices to the related fields
    def __init__(self, *args,**kwargs):
        super(AddNewProductionRunForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name)
                                     for product in Product.query.order_by(Product.name).all()]

class EditProductionRunForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    flour_kneaded = IntegerField('Flour Kneaded')
    oil_used = IntegerField('Oil used')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Edit')

    # adding choices to the related fields
    def __init__(self, *args,**kwargs):
        super(EditProductionRunForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name)
                                     for product in Product.query.order_by(Product.name).all()]
        

class AddNewIngredient(FlaskForm):
    name = StringField("Ingredient Name", validators=[DataRequired()])
    measurement = StringField("Unit of Measurement")
    submit = SubmitField("Add")


class AddNewSupplier(FlaskForm):
    name = StringField("Supplier Name", validators=[DataRequired()])
    phone_no = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email")
    submit = SubmitField("Add")