from flask import render_template, redirect, request, url_for, flash
from . import product_raw
from .forms import SearchForm
from app.models import ProductRaw
from flask_login import login_required, current_user
import json, datetime

# List Product Raw
@product_raw.route('/product_raw', methods=['GET', 'POST'])
@login_required
def functionGetProductRaw():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        product_raw = ProductRaw.select() \
                .where(
                    ProductRaw.product_raw_code.contains(form.search.data)
                    | ProductRaw.product_raw_name.contains(form.search.data)
                    | ProductRaw.product_raw_description.contains(form.search.data)
                )
    else:
        product_raw = ProductRaw.select().execute()

    return render_template('product_raw/list_product_raw.html', current_user=current_user, form=form, len_list=len(product_raw), list_product_raw=product_raw)

# Get Product Raw
@product_raw.route('/getProductRawByID', methods=['POST'])
@login_required
def functionGetProductRawByID():
    id = request.form['id']
    # Get User By ID
    productRaw = ProductRaw.get_by_id(id)

    product_raw_row = {
        "product_raw_id": productRaw.id,
        "product_raw_name": productRaw.product_raw_name,
        "product_raw_code": productRaw.product_raw_code,
        "product_raw_description": productRaw.product_raw_description,
        "product_raw_amount": productRaw.amount
    }

    return product_raw_row

# Get Latest Product Code
@product_raw.route('/getProductRawCode', methods=['POST'])
@login_required
def functionGetProductRawCode():
    # Get User By ID
    product = ProductRaw.select().order_by(ProductRaw.id.desc()).first()

    product_code = "1"
    if product != None:
        product_code = str(product.id + 1)

    product_code = "PDR-" + product_code.zfill(6)
    return product_code

# Insert Product Raw (with modal)
@product_raw.route('/insertProductRaw', methods=['GET', 'POST'])
@login_required
def functionInsertProductRaw():
    row = {
        "status": "success",
        "message": "Success"
    }

    product_raw_code = request.form['product_raw_code']
    product_raw_name = request.form['product_raw_name']
    product_raw_description = request.form['product_raw_description']
    product_raw_amount = request.form['product_raw_amount']

    try:
        productRaw = ProductRaw.insert(
            product_raw_code=product_raw_code,
            product_raw_name=product_raw_name,
            product_raw_description=product_raw_description,
            amount=product_raw_amount,
            created_by=current_user.id,
            created_at=datetime.datetime.now()
        ).execute()

        row['status'] = "success"
        row['message'] = "Successfully Inserted"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Insert"

    return row

# Update Product Raw
@product_raw.route('/updateProductRaw', methods=['GET', 'POST'])
@login_required
def functionUpdateProductRaw():
    row = {
        "status": "success",
        "message": "Success"
    }

    id = request.form['id']
    product_raw_name = request.form['product_raw_name']
    product_raw_description = request.form['product_raw_description']
    product_raw_amount = request.form['product_raw_amount']

    try:
        query_user = ProductRaw.get_by_id(id)
        if query_user == None:
            row['status'] = "danger"
            row['message'] = "User not exist"
        else:
            try:
                query_update = ProductRaw.update(
                    product_raw_name=product_raw_name,
                    product_raw_description=product_raw_description,
                    amount=product_raw_amount,
                    updated_by=current_user.id,
                    updated_at=datetime.datetime.now()
                )
                query_update.where(ProductRaw.id == id).execute()

                row['status'] = "success"
                row['message'] = "Successfully Updated"
            except Exception as e:
                row['status'] = "danger"
                row['message'] = "Failed to Update"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Update"

    return row

# Delete Product Raw
@product_raw.route('/deleteProductRawByID', methods=['POST'])
@login_required
def functionDeleteProductRawByID():
    row = {
        "status": "success",
        "message": "Success"
    }

    form = SearchForm()

    id = request.form['id']
    # Delete Product By ID
    try:
        ProductRaw.delete_by_id(id)

        row['status'] = "success"
        row['message'] = "Successfully Deleted"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Delete"

    return row