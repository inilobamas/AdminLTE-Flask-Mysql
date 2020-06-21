from flask import render_template, redirect, request, url_for, flash
from . import detail_memorandum
from .forms import SearchForm
from app.models import DetailMemorandum
from flask_login import login_required, current_user
import json, datetime

# # List Memorandum
# @detail_memorandum.route('/detail_memorandum', methods=['GET', 'POST'])
# @login_required
# def functionGetDetailMemorandum():
#     form = SearchForm()
#     # if request.method == 'POST' and form.validate_on_submit():
#     #     user = User.select()\
#     #         .where(
#     #             User.username.contains(form.search.data)
#     #             | User.fullname.contains(form.search.data)
#     #             | User.email.contains(form.search.data)
#     #             | User.address.contains(form.search.data)
#     #             | User.phone.contains(form.search.data)
#     #             | User.role.contains(form.search.data)
#     #         )
#     # else:
#     #     user = User.select().execute()
#
#     return render_template('detail_memorandum/list_detail_memorandum.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)