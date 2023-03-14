from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email
from ..models import User


class SignUpForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Regexp('^[A-Za-z ]*$', 0, 'Name must only contain letters.')], render_kw={"placeholder":"Fullname"})
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must only contain letters, numbers, dots or underscores.')], render_kw={"placeholder":"Username"})
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')], render_kw={"placeholder":"Password"})
    password2 = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists')


class LogInForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Length(1, 128), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')