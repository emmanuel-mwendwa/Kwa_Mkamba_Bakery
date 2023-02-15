from . import auth
from .forms import SignUpForm, LogInForm
from flask import render_template


@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    return render_template('auth/sign_up.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    return render_template('auth/login.html', form=form)