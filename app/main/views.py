from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Role
from ..decorators import admin_required, permission_required

@main.route('/home')
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return render_template('user.html', user=user)
    else:
        abort(403)
        
@main.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone_no = form.phone_no.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', category='success')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.phone_no.data = current_user.phone_no
    return render_template('edit_profile.html', form=form)

@main.route('/edit_profile/<int:id>', methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.phone_no = form.phone_no.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.', category='success')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.phone_no.data = user.phone_no
    return render_template('edit_profile.html', form=form, user=user)