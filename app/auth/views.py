from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from .forms import LoginForm, SignUpForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..main.forms import EditProfileForm
from ..models import User
from ..email import send_email
from flask_login import login_user, logout_user, login_required, current_user

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    profile_form = EditProfileForm()
    if form.validate_on_submit() and profile_form.validate_on_submit():
        user = User(
            email=form.email.data.lower(), 
            username=form.username.data, 
            password=form.password.data, 
            name=profile_form.name.data, 
            phone_no=profile_form.phone_no.data
            )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form, profile_form=profile_form)

@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password', category='error')
    return render_template('/auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

# confirm user
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Thank you for confirming your account', category='success')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

# run before everything else in the application
@auth.before_app_request
def before_request():
    if current_user.is_authenticated\
        and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

# redirect user to this page if user is unconfirmed
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

# resend confirmation links
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you.', category='success')
    return redirect(url_for('main.index'))

# update passwords
@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated successfully.', category='success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid Password', category='error')
    return render_template('auth/change_password.html', form=form)

# reset password
@auth.route('/reset', methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password', 'auth/email/reset_password', user=user, token=token)
        flash('An email with instructions to reset your password has been sent to you.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.', category='success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

# change email address
@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.', category='success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', category='error')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.', category='success')
    else:
        flash('Invalid request.', category='error')
    return redirect(url_for('main.index'))