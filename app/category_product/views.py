from flask import render_template, redirect, request, url_for, flash
from . import category_product
from .forms import SearchForm
from app.models import CategoryProduct
from flask_login import login_required, current_user
import json, datetime


# Get Product
@category_product.route('/getCateogryProductDropdown', methods=['POST'])
@login_required
def functionGetCategoryProductDropdown():
    # Get User By ID
    category_product = CategoryProduct.get_by_id(id)

    category_product_row = {
        "category_product_name": category_product.category_product_name,
        "category_product_description": category_product.category_product_description
    }

    return category_product_row

# # List Product
# @product.route('/product', methods=['GET', 'POST'])
# @login_required
# def functionGetProduct():
#     form = SearchForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         product = Product.select()\
#             .where(
#                 Product.product_code.contains(form.search.data)
#                 | Product.product_name.contains(form.search.data)
#                 | Product.description.contains(form.search.data)
#             )
#     else:
#         product = Product.select().execute()
#
#     return render_template('product/list_product.html', current_user=current_user, form=form, len_list=len(product), list_product=product)
#
# # Get Product
# @product.route('/getProductByID', methods=['POST'])
# @login_required
# def functionGetProductByID():
#     id = request.form['id']
#     # Get User By ID
#     product = Product.get_by_id(id)
#
#     product_row = {
#         "product_code": product.product_code,
#         "product_name": product.product_name,
#         "description": product.description,
#         "price": product.price
#     }
#
#     return product_row
#
# # Get Latest Product Code
# @product.route('/getProductCode', methods=['POST'])
# @login_required
# def functionGetProductCode():
#     # Get User By ID
#     product = Product.select().order_by(Product.id.desc()).first()
#
#     product_code = "1"
#     if product != None:
#         product_code = str(product.id + 1)
#
#     product_code = "PD-" + product_code.zfill(6)
#     return product_code
#
# # Insert Product (with modal)
# @product.route('/insertProduct', methods=['GET', 'POST'])
# @login_required
# def functionInsertProduct():
#     row = {
#         "status": "success",
#         "message": "Success"
#     }
#
#     product_code = request.form['product_code']
#     product_name = request.form['product_name']
#     description = request.form['description']
#     price = request.form['price']
#
#     try:
#         product = Product.insert(
#             product_code=product_code,
#             product_name=product_name,
#             description=description,
#             price=price,
#             created_by=current_user.id,
#             created_at=datetime.datetime.now()
#         ).execute()
#
#         row['status'] = "success"
#         row['message'] = "Successfully Inserted"
#     except Exception as e:
#         row['status'] = "danger"
#         row['message'] = "Failed to Insert"
#
#     return row
#
# # Update Product
# @product.route('/updateProduct', methods=['GET', 'POST'])
# @login_required
# def functionUpdateProduct():
#     row = {
#         "status": "success",
#         "message": "Success"
#     }
#
#     id = request.form['id']
#     product_name = request.form['product_name']
#     description = request.form['description']
#     price = request.form['price']
#
#     try:
#         query_user = Product.get_by_id(id)
#         if query_user == None:
#             row['status'] = "danger"
#             row['message'] = "User not exist"
#         else:
#             try:
#                 query_update = Product.update(
#                     product_name=product_name,
#                     description=description,
#                     price=price,
#                     updated_by=current_user.id,
#                     updated_at=datetime.datetime.now()
#                 )
#                 query_update.where(Product.id == id).execute()
#
#                 row['status'] = "success"
#                 row['message'] = "Successfully Updated"
#             except Exception as e:
#                 row['status'] = "danger"
#                 row['message'] = "Failed to Update"
#     except Exception as e:
#         row['status'] = "danger"
#         row['message'] = "Failed to Update"
#
#     return row
#
# # Delete Product
# @product.route('/deleteProductByID', methods=['POST'])
# @login_required
# def functionDeleteProductByID():
#     row = {
#         "status": "success",
#         "message": "Success"
#     }
#
#     form = SearchForm()
#
#     id = request.form['id']
#     # Delete Product By ID
#     try:
#         Product.delete_by_id(id)
#
#         row['status'] = "success"
#         row['message'] = "Successfully Deleted"
#     except Exception as e:
#         row['status'] = "danger"
#         row['message'] = "Failed to Delete"
#
#     # Get All User
#     product = Product.select().execute()
#
#     return render_template('product/list_product.html', current_user=current_user, form=form, len_list=len(product), list_product=product)