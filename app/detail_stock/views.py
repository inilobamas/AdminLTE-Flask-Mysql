from flask import render_template, redirect, request, url_for, flash
from . import detail_stock
from .forms import SearchForm
from app.models import DetailStock
from flask_login import login_required, current_user
import json, datetime

# List Stock
@detail_stock.route('/detail_stock', methods=['GET', 'POST'])
@login_required
def functionGetDetailStock():
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

    return render_template('detail_stock/list_detail_stock.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)