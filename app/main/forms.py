from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddProductsForm(FlaskForm):
    code = StringField('Product Code', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    price = IntegerField('Product Price', validators=[DataRequired()])
    submit = SubmitField('Add Product')