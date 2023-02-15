from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email
from ..models import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must only contain letters, numbers, dots or underscores.')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')