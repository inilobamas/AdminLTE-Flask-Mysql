from flask import render_template, redirect, request, url_for, flash
from . import user_account
from .forms import SearchForm
from app.models import UserAccount
from flask_login import login_required, current_user
import json, datetime

# List User Account
@user_account.route('/user_account', methods=['GET', 'POST'])
@login_required
def functionGetUserAccount():
    form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     user = User.select()\
    #         .where(
    #             User.username.contains(form.search.data)
    #             | User.fullname.contains(form.search.data)
    #             | User.email.contains(form.search.data)
    #             | User.address.contains(form.search.data)
    #             | User.phone.contains(form.search.data)
    #             | User.role.contains(form.search.data)
    #         )
    # else:
    #     user = User.select().execute()

    return render_template('user_account/list_user_account.html', current_user=current_user, form=form) # len_list=len(user), list_user=user,

# Add User Account
@user_account.route('/add_user_account', methods=['GET', 'POST'])
@login_required
def functionAddUserAccount():
    form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     user = User.select()\
    #         .where(
    #             User.username.contains(form.search.data)
    #             | User.fullname.contains(form.search.data)
    #             | User.email.contains(form.search.data)
    #             | User.address.contains(form.search.data)
    #             | User.phone.contains(form.search.data)
    #             | User.role.contains(form.search.data)
    #         )
    # else:
    #     user = User.select().execute()

    return render_template('user_account/add_user_account.html', current_user=current_user, form=form) # len_list=len(user), list_user=user,