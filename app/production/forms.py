from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError

class AddNewProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Add New Product")