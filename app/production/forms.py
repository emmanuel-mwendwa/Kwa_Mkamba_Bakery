from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, IntegerField, FloatField, SelectMultipleField, widgets, FormField, FieldList
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
        

class AddNewIngredient(FlaskForm):
    name = StringField("Ingredient Name", validators=[DataRequired()])
    measurement = StringField("Unit of Measurement")
    submit = SubmitField("Submit")

class AddSupplierIngredientForm(FlaskForm):
    ingredient_id = SelectField('Ingredient', coerce=int)
    unit_cost = FloatField('Unit Cost')

    # adding choices to the related fields
    def __init__(self, *args,**kwargs):
        super(AddSupplierIngredientForm, self).__init__(*args, **kwargs)

        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                     for ingredient in Ingredient.query.order_by(Ingredient.name).all()]
        

class AddNewSupplier(FlaskForm):
    name = StringField("Supplier Name", validators=[DataRequired()])
    phone_no = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email")
    ingredients = FieldList(FormField(AddSupplierIngredientForm), min_entries=1)
    submit = SubmitField("Submit")

    def add_empty_ingredient(self):
        empty_ingredient = AddSupplierIngredientForm()
        self.ingredients.append_entry(empty_ingredient)
     

class RecipeIngredientForm(FlaskForm):
    ingredient_id = SelectField('Ingredient', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    unit_of_measurement = StringField('Unit of Measurement', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.ingredient_id.choices = [(0, 'Select an Ingredient')] + [(ingredient.id, ingredient.name)
                                     for ingredient in Ingredient.query.order_by(Ingredient.name).all()]


class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    yield_amount = IntegerField('Yield Amount', validators=[DataRequired()])
    recipe_ingredients = FieldList(FormField(RecipeIngredientForm), min_entries=1)
    submit = SubmitField("Submit")

    def add_empty_ingredient(self):
        empty_ingredient = RecipeIngredientForm()
        self.recipe_ingredients.append_entry(empty_ingredient)
