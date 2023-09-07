from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        render_kw={'placeholder': 'Email'}, 
                        validators=[DataRequired(), Length(1, 64), Email()]
                        )
    password = PasswordField('Password',
                            render_kw={'placeholder': 'Password'},  
                            validators=[DataRequired()]
                            )
    remember_me = BooleanField('Keep me logged in', default=True)
    submit = SubmitField('Log In')


class SignUpForm(FlaskForm):
    email = StringField('Email',
                        render_kw={'placeholder': 'Email'}, 
                        validators=[DataRequired(), Length(1, 64), Email()]
                        )
    username = StringField('Username',
                        render_kw={'placeholder': 'Username'},
                        validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames can only contain letters, numbers, dots or underscores')]
                        )
    password = PasswordField('Password',
                            render_kw={'placeholder': 'Password'},
                            validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')]
                            )
    password2 = PasswordField('Confirm Password',
                            render_kw={'placeholder': 'Confirm Password'},
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
        

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',
                                render_kw={'placeholder': 'Old Password'},
                                validators=[DataRequired()]
                                )
    password = PasswordField('New Password',
                            render_kw={'placeholder': 'New Password'},
                            validators=[DataRequired(), EqualTo('password2', message='Passwords must match')]
                            )
    password2 = PasswordField('Confirm Password',
                              render_kw={'placeholder': 'Confirm Password'},
                              validators=[DataRequired()]
                              )
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        render_kw={'placeholder': 'Email'},
                        validators=[DataRequired(), Length(1, 64), Email()]
                        )
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', 
                            render_kw={'placeholder': 'New Password'},
                            validators=[DataRequired(), EqualTo('password2', message='Passwords must match')]
                            )
    password2 = PasswordField('Confirm password',
                            render_kw={'placeholder': 'Confirm Password'},
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email',
                        render_kw={'placeholder': 'New Email'},
                        validators=[DataRequired(), Length(1, 64), Email()]
                        )
    password = PasswordField('Password',
                            render_kw={'placeholder': 'Password'},
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')