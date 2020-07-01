from flask import render_template, redirect, request, url_for, flash
from . import detail_product_raw
from .forms import SearchForm
from app.models import ProductRaw, DetailProductRaw, DetailStock, Product, User, Memorandum, DetailMemorandum
from flask_login import login_required, current_user
from ..helper.views import formatrupiah
import json, datetime

# List Product Raw
@detail_product_raw.route('/detail_product_raw', methods=['GET', 'POST'])
@login_required
def functionGetDetailProductRaw():
    form = SearchForm()
    product_raw_id = request.args.get('id')

    product = DetailProductRaw.select(DetailProductRaw, Product)\
        .join(Product, on=(Product.id == DetailProductRaw.product_id))\
        .where(DetailProductRaw.product_raw_id == product_raw_id)

    total=0
    for row in product:
        total = total + row.amount

    product_raw = ProductRaw.get_by_id(product_raw_id)
    sisa = product_raw.amount - total
    sisa = formatrupiah(sisa)
    total = formatrupiah(total)
    product_raw.amount = formatrupiah(product_raw.amount)

    return render_template('detail_product_raw/list_detail_product_raw.html', current_user=current_user, form=form, product_raw=product_raw, len_product=len(product), product=product, total=total, sisa=sisa)