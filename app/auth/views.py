from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required
import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.get(User.username == form.username.data)
                if user.verify_password(form.password.data):
                    login_user(user, form.rememberme.data)
                    flash('Successfully Logged', 'success')
                    return redirect(request.args.get('next') or url_for('main.index'))
                else:
                    flash('Wrong user name or password', 'danger')
            except:
                flash('Wrong user name or password', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'warning')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                query_user = User.select().where(User.username == form.username.data)
                if query_user.exists():
                    flash('Username already exist', 'danger')
                    print("Username already exist")
                else:
                    try:
                        # Hash password first
                        password_hashed = User.generate_password(None, form.password.data)
                    except Exception as e:
                        flash('Error generate password', 'danger')

                    try:
                        new_user = User(username=form.username.data,
                                        password=password_hashed,
                                        fullname=form.fullname.data,
                                        email=form.email.data,
                                        phone=form.phone.data,
                                        address=form.address.data,
                                        role="admin",
                                        status=1,
                                        created_at=datetime.datetime.now(),
                                        created_by=0)
                        new_user.save()

                        return redirect(url_for('auth.login'))
                    except Exception as e:
                        flash('Failed insert to user', 'danger')
            except Exception as e:
                flash('Failed to validate', 'danger')
        else:
            flash('Failed to validate', 'danger')
    return render_template('auth/register.html', form=form)