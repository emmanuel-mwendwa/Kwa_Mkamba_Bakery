from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SelectField, SubmitField, FloatField, FormField, FieldList
from wtforms.validators import DataRequired, Regexp, Email, Length
from wtforms import ValidationError
from ..models import User, Customer, Route, Product

class AddNewCustomerForm(FlaskForm):
    cust_name = StringField("Customer Name: ", validators=[DataRequired(), Length(0, 64), Regexp('^[A-Za-z ]*$',0, 'Names can only contain letters and spaces')])
    cust_email = StringField("Customer Email: ", validators=[DataRequired(), Length(1, 64), Email()])
    cust_phone_no = StringField('Phone Number: ', validators=[Length(0, 13), Regexp('^[0-9+]*$', 0, 'Phonw number can only contain numbers')])
    cust_mpesa_agent_name = StringField("Mpesa Name: ", validators=[])
    route_id = SelectField('Route', coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(AddNewCustomerForm, self).__init__(*args, **kwargs)
        self.route_id.choices = [(route.route_id, route.route_name)
                                 for route in Route.query.all()]

    def validate_cust_email(self, field):
        if Customer.query.filter_by(cust_email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_phone_no(self, field):
        if field.data:
            if field.data.startswith('0'):
                field.data = field.data[1:]
                field.data = '+254' + field.data
            elif not field.data.startswith('+'):
                field.data = '+' + field.data


class AddNewRouteForm(FlaskForm):
    route_name = StringField('Route Name', validators=[DataRequired(), Length(0, 64), Regexp('^[A-Za-z_ ]*$',0,'Route names can only contain letters, spaces and underscores')])
    sales_assoc_id = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


    def __init__(self, *args, **kwargs):
        super(AddNewRouteForm, self).__init__(*args, **kwargs)
        self.sales_assoc_id.choices = [(user.id, user.name)
                                       for user in User.query.filter_by(role_id=3).all()]
        

class DispatchDetailsForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)
    quantity = FloatField('Quantity')
    returns = FloatField('Returns')

    def __init__(self, *args, **kwargs):
        super(DispatchDetailsForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(0, 'Select a product')] + [(product.id, product.name)
                                                               for product in Product.query.order_by(Product.name).all()]


class DispatchForm(FlaskForm):
    sales_assoc_name = SelectField('Sales Agent', coerce=int)
    # route_name = SelectField("Route", coerce=int)
    dispatch_details = FieldList(FormField(DispatchDetailsForm), min_entries=2)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(DispatchForm, self).__init__(*args, **kwargs)
        self.sales_assoc_name.choices = [(sales_assoc.id, sales_assoc.name)
                                         for sales_assoc in User.query.filter_by(role_id=3).all()]

    def add_empty_dispatch(self):
        empty_dispatch = DispatchDetailsForm()
        self.dispatch_details.append_entry(empty_dispatch)