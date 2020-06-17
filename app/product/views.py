from flask import render_template, redirect, request, url_for, flash
from . import product
from .forms import SearchForm
from app.models import Product, CategoryProduct, ProductRaw, Stock
from flask_login import login_required, current_user
import json, datetime

# List Product
@product.route('/product', methods=['GET', 'POST'])
@login_required
def functionGetProduct():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        product = Product.select(Product, CategoryProduct, ProductRaw, Stock) \
            .join(CategoryProduct, on=(Product.category_product_id == CategoryProduct.id)) \
            .switch(Product) \
            .join(ProductRaw, on=(Product.product_raw_id == ProductRaw.id)) \
            .switch(Product) \
            .join(Stock, on=(Stock.product_id == Product.id)) \
            .where(
                Product.product_code.contains(form.search.data)
                | Product.product_name.contains(form.search.data)
                | Product.description.contains(form.search.data)
                | CategoryProduct.category_product_name.contains(form.search.data)
            )
    else:
        product = Product.select(Product, CategoryProduct, ProductRaw, Stock)\
            .join(CategoryProduct, on=(Product.category_product_id == CategoryProduct.id)) \
            .switch(Product) \
            .join(ProductRaw, on=(Product.product_raw_id == ProductRaw.id)) \
            .switch(Product) \
            .join(Stock, on=(Stock.product_id == Product.id)) \
            .execute()

    category_product = CategoryProduct.select().execute()
    product_raw = ProductRaw.select().execute()

    return render_template('product/list_product.html', current_user=current_user, form=form, len_list=len(product), list_product=product, len_dropdown_category_product=len(category_product), dropdown_category_product=category_product, len_product_raw=len(product_raw), dropdown_product_raw=product_raw)

# Get Product
@product.route('/getProductByID', methods=['POST'])
@login_required
def functionGetProductByID():
    id = request.form['id']
    # Get User By ID
    product = Product.get_by_id(id)

    product_row = {
        "product_raw_id": product.product_raw_id,
        "category_product_id": product.category_product_id,
        "product_code": product.product_code,
        "product_name": product.product_name,
        "description": product.description,
        "price": product.price
    }

    return product_row

# Get Latest Product Code
@product.route('/getProductCode', methods=['POST'])
@login_required
def functionGetProductCode():
    # Get User By ID
    product = Product.select().order_by(Product.id.desc()).first()

    product_code = "1"
    if product != None:
        product_code = str(product.id + 1)

    product_code = "PD-" + product_code.zfill(6)
    return product_code

# Insert Product (with modal)
@product.route('/insertProduct', methods=['GET', 'POST'])
@login_required
def functionInsertProduct():
    row = {
        "status": "success",
        "message": "Success"
    }

    product_raw_id = request.form['product_raw_id']
    category_product_id = request.form['category_product_id']
    product_code = request.form['product_code']
    product_name = request.form['product_name']
    description = request.form['description']
    price = request.form['price']

    try:
        product = Product.insert(
            product_code=product_code,
            product_name=product_name,
            description=description,
            price=price,
            created_by=current_user.id,
            created_at=datetime.datetime.now()
        ).execute()

        row['status'] = "success"
        row['message'] = "Successfully Inserted"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Insert"

    return row

# Update Product
@product.route('/updateProduct', methods=['GET', 'POST'])
@login_required
def functionUpdateProduct():
    row = {
        "status": "success",
        "message": "Success"
    }

    id = request.form['id']
    product_name = request.form['product_name']
    description = request.form['description']
    price = request.form['price']

    try:
        query_user = Product.get_by_id(id)
        if query_user == None:
            row['status'] = "danger"
            row['message'] = "User not exist"
        else:
            try:
                query_update = Product.update(
                    product_name=product_name,
                    description=description,
                    price=price,
                    updated_by=current_user.id,
                    updated_at=datetime.datetime.now()
                )
                query_update.where(Product.id == id).execute()

                row['status'] = "success"
                row['message'] = "Successfully Updated"
            except Exception as e:
                row['status'] = "danger"
                row['message'] = "Failed to Update"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Update"

    return row

# Delete Product
@product.route('/deleteProductByID', methods=['POST'])
@login_required
def functionDeleteProductByID():
    row = {
        "status": "success",
        "message": "Success"
    }

    form = SearchForm()

    id = request.form['id']
    # Delete Product By ID
    try:
        Product.delete_by_id(id)

        row['status'] = "success"
        row['message'] = "Successfully Deleted"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Delete"

    return row