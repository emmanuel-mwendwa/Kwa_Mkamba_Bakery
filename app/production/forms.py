from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, IntegerField, FloatField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import ValidationError
from ..models import Product, Supplier, Ingredient

class AddNewProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Submit")


class AddNewProductionRunForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    flour_kneaded = IntegerField('Flour Kneaded')
    oil_used = IntegerField('Oil used')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')

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
    submit = SubmitField('Update')

    # adding choices to the related fields
    def __init__(self, *args,**kwargs):
        super(EditProductionRunForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name)
                                     for product in Product.query.order_by(Product.name).all()]
        

class AddNewIngredient(FlaskForm):
    name = StringField("Ingredient Name", validators=[DataRequired()])
    measurement = StringField("Unit of Measurement")
    submit = SubmitField("Submit")


class AddNewSupplier(FlaskForm):
    name = StringField("Supplier Name", validators=[DataRequired()])
    phone_no = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email")
    submit = SubmitField("Submit")


class EditSupplier(FlaskForm):
    name = StringField("Supplier Name", validators=[DataRequired()])
    phone_no = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email")
    submit = SubmitField("Update")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddSupplierIngredientForm(FlaskForm):
    supplier_id = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    ingredient_id = SelectField('Ingredient', coerce=int)
    unit_cost = FloatField('Unit Cost')
    submit = SubmitField('Submit')

    # adding choices to the related fields
    def __init__(self, *args,**kwargs):
        super(AddSupplierIngredientForm, self).__init__(*args, **kwargs)
        self.supplier_id.choices = [(supplier.id, supplier.name)
                                     for supplier in Supplier.query.order_by(Supplier.name).all()]
    
        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                     for ingredient in Ingredient.query.order_by(Ingredient.name).all()]
        

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    yield_amount = IntegerField('Yield Amount', validators=[DataRequired()])


class RecipeIngredientForm(FlaskForm):
    ingredient_id = SelectField('Ingredient', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    unit_of_measurement = StringField('Unit of Measurement', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                     for ingredient in Ingredient.query.order_by(Ingredient.name).all()]
    