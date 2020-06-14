from flask import render_template, redirect, request, url_for, flash

from . import stock
from .forms import SearchForm
from app.models import Stock, Product
from flask_login import login_required, current_user
import json, datetime

# List Stock
@stock.route('/stock', methods=['GET', 'POST'])
@login_required
def functionGetStock():
    form = SearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        stock = Stock.select(Product.id.alias('product_id'),
                             Product.product_name.alias('product_name'),
                             Product.product_code.alias('product_code'),
                             Product.description.alias('product_description'),
                             Product.price.alias('product_price'),
                             Stock.id.alias('stock_id'),
                             Stock.amount.alias('stock_amount'))\
            .join(Product, on=(Stock.product_id == Product.id))\
            .where(
                Product.product_code.contains(form.search.data)
                | Product.product_name.contains(form.search.data)
                | Product.description.contains(form.search.data)
            )
    else:
        stock = Stock.select(Product.id.alias('product_id'),
                             Product.product_name.alias('product_name'),
                             Product.product_code.alias('product_code'),
                             Product.description.alias('product_description'),
                             Product.price.alias('product_price'),
                             Stock.id.alias('stock_id'),
                             Stock.amount.alias('stock_amount')
                             ).join(Product, on=(Stock.product_id == Product.id))

    return render_template('stock/list_stock.html', current_user=current_user, form=form, len_list=len(stock), list_stock=stock)