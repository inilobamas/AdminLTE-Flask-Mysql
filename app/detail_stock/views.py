from flask import render_template, redirect, request, url_for, flash
from . import detail_stock
from .forms import SearchForm
from app.models import DetailStock, Product, User
from flask_login import login_required, current_user
import json, datetime

# List Stock
@detail_stock.route('/detail_stock', methods=['GET', 'POST'])
@login_required
def functionGetDetailStock():
    product_id = request.args.get('product_id')
    stock_id = request.args.get('stock_id')

    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        # user = User.select()\
        #     .where(
        #         User.username.contains(form.search.data)
        #         | User.fullname.contains(form.search.data)
        #         | User.email.contains(form.search.data)
        #         | User.address.contains(form.search.data)
        #         | User.phone.contains(form.search.data)
        #         | User.role.contains(form.search.data)
        #     )
        detail_stock = DetailStock.select(User, DetailStock).join(User, on=(User.id == DetailStock.user_id)).where(DetailStock.stock_id == stock_id).execute()
    else:
        detail_stock = DetailStock.select(User, DetailStock).join(User, on=(User.id == DetailStock.user_id)).where(DetailStock.stock_id == stock_id).execute()

    if product_id != "":
        product = Product.get_by_id(product_id)
    else:
        return redirect(url_for('product.functionGetProduct'))

    return render_template('detail_stock/list_detail_stock.html', current_user=current_user, form=form, data_product=product, len_list=len(detail_stock), list_detail_stock=detail_stock) #, len_list=len(product), list_user=user)