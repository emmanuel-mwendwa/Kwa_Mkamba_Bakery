from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, Length
from wtforms import ValidationError
from ..models import User, Customer

class AddNewCustomerForm(FlaskForm):
    cust_name = StringField("Customer Name: ", validators=[DataRequired(), Length(0, 64), Regexp('^[A-Za-z ]*$',0, 'Names can only contain letters and spaces')])
    cust_email = StringField("Customer Email: ", validators=[DataRequired(), Length(1, 64), Email()])
    cust_phone_no = StringField('Phone Number: ', validators=[Length(0, 13), Regexp('^[0-9+]*$', 0, 'Phonw number can only contain numbers')])
    cust_mpesa_agent_name = StringField("Mpesa Name: ", validators=[])
    submit = SubmitField("Submit")


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
