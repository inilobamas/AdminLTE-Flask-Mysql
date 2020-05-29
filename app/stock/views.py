from flask import render_template, redirect, request, url_for, flash
from . import stock
from app.product import product
from .forms import SearchForm
from app.models import Stock
from flask_login import login_required, current_user
import json, datetime

# List Stock
@stock.route('/stock', methods=['GET', 'POST'])
@login_required
def functionGetStock():
    form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     stock = Stock.select()\
    #         .join(Product, on=(Tweet.user == User.id))\
    #         .where(
    #             User.username.contains(form.search.data)
    #             | User.fullname.contains(form.search.data)
    #             | User.email.contains(form.search.data)
    #             | User.address.contains(form.search.data)
    #             | User.phone.contains(form.search.data)
    #             | User.role.contains(form.search.data)
    #         )
    # else:
    #     stock = Stock.select().execute()

    return render_template('stock/list_stock.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)