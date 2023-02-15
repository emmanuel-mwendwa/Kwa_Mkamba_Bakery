from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9]._', 0, 'Username must only contain letters, numbers, dots or underscores.')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')