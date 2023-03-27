from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from ..models import Product, Production_Run

class AddNewProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Add New Product")


class AddNewProductionRunForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    flour_kneaded = StringField('Flour Kneaded')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Add New ProductionRun')

    def __init__(self, *args,**kwargs):
        super(AddNewProductionRunForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name)
                                     for product in Product.query.order_by(Product.name).all()]
