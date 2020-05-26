from flask import render_template, redirect, request, url_for, flash
from . import memorandum
from .forms import SearchForm
from app.models import Memorandum
from flask_login import login_required, current_user
import json, datetime

# List Memorandum
@memorandum.route('/memorandum', methods=['GET', 'POST'])
@login_required
def functionGetMemorandum():
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

    return render_template('memorandum/list_memorandum.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)

# Add Memorandum
@memorandum.route('/add_memorandum', methods=['GET', 'POST'])
@login_required
def functionAddMemorandum():
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

    return render_template('memorandum/add_memorandum.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)

# Add Memorandum
@memorandum.route('/add_memorandum2', methods=['GET', 'POST'])
@login_required
def functionAddMemorandum2():
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

    return render_template('memorandum/add_memorandum2.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)