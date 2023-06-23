from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, Length
from wtforms import ValidationError
from ..models import User

class AddNewCustomerForm(FlaskForm):
    cust_name = StringField("Customer Name: ", validators=[DataRequired(), Length(0, 64), Regexp('^[A-Za-z ]*$',0, 'Names can only contain letters and spaces')])
    cust_email = StringField("Customer Email: ", validators=[DataRequired(), Length(1, 64), Email()])
    cust_phone_no = StringField('Phone Number: ', validators=[Length(0, 13), Regexp('^[0-9+]*$', 0, 'Phonw number can only contain numbers')])
    cust_mpesa_agent_name = StringField("Mpesa Name: ", validators=[])
    submit = SubmitField("Submit")


    def validate_email(self, field):
        if field.data != self.user.email and\
        User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_phone_no(self, field):
        if field.data:
            if field.data.startswith('0'):
                field.data = field.data[1:]
                field.data = '+254' + field.data
            elif not field.data.startswith('+'):
                field.data = '+' + field.data
