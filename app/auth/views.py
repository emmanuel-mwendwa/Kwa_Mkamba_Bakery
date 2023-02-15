from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from .forms import SignUpForm, LogInForm
from ..models import User


@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/sign_up.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!!')
    return redirect(url_for('main.index'))