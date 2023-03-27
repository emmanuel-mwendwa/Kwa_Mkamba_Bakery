from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms import ValidationError
from ..models import Role, User

class EditProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[Length(0, 64), Regexp('^[A-Za-z ]*$',0, 'Names can only contain letters and spaces')])
    phone_no = StringField('Phone Number', validators=[Length(0, 13), Regexp('^[0-9+]*$',0, 'Phone number can only contain numbers')])
    submit = SubmitField('Submit')

    def validate_phone_no(self, field):
        if field.data:
            if field.data.startswith('0'):
                field.data = field.data[1:]
                field.data = '+254' + field.data
            elif not field.data.startswith('+'):
                field.data = '+' + field.data


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Full Name', validators=[Length(0, 64), Regexp('^[A-Za-z ]*$',0, 'Names can only contain letters and spaces')])
    phone_no = StringField('Phone Number', validators=[Length(0, 13), Regexp('^[0-9+]*$',0, 'Phone number can only contain numbers')])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and\
        User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if field.data != self.user.username and\
        User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
        
    def validate_phone_no(self, field):
        if field.data:
            if field.data.startswith('0'):
                field.data = field.data[1:]
                field.data = '+254' + field.data
            elif field.data.startswith('254'):
                field.data = field.data[3:]
                field.data = '+254' + field.data
            if not field.data.startswith('+'):
                field.data = '+' + field.data
