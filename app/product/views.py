from flask import render_template, redirect, request, url_for, flash
from . import product
from .forms import SearchForm
from app.models import Product, CategoryProduct, ProductRaw, Stock
from flask_login import login_required, current_user
from peewee import MySQLDatabase, JOIN
from conf.config import config
import os, json, datetime

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


# List Product
@product.route('/product', methods=['GET', 'POST'])
@login_required
def functionGetProduct():
    form = SearchForm()
    product = []
    if request.method == 'POST' and form.validate_on_submit():
        product_query = "SELECT " \
                        "t1.id AS product_id, " \
                        "t1.category_product_id AS category_product_id, " \
                        "t1.product_code AS product_code, " \
                        "t1.product_name AS product_name, " \
                        "t1.description AS product_description, " \
                        "t1.price AS product_price, " \
                        "t1.created_at AS product_created_at, " \
                        "t1.created_by AS product_created_by, " \
                        "t1.updated_at AS product_updated_at, " \
                        "t1.updated_by AS product_updated_by, " \
                        "t2.id AS category_product_id, " \
                        "t2.category_product_name AS category_product_name, " \
                        "t2.category_product_description AS category_product_description, " \
                        "t2.created_at AS category_product_created_at, " \
                        "t2.created_by AS category_product_created_by, " \
                        "t2.updated_at AS category_product_updated_at, " \
                        "t2.updated_by AS category_product_updated_by, " \
                        "t4.id AS stock_id, " \
                        "t4.product_id AS stock_product_id, " \
                        "t4.amount AS stock_amount, " \
                        "t4.created_at AS stock_created_at, " \
                        "t4.created_by AS stock_created_by, " \
                        "t4.updated_at AS stock_updated_at, " \
                        "t4.updated_by AS stock_updated_by " \
                        "FROM product AS t1 " \
                        "INNER JOIN categoryproduct AS t2 ON (t2.id = t1.category_product_id) " \
                        "LEFT JOIN stock AS t4 ON (t4.product_id = t1.id) " \
                        "WHERE " \
                        "product.product_code LIKE '%" + form.search.data + "%' or" \
                        "product.product_name LIKE '%" + form.search.data + "%' or" \
                        "product.description LIKE '%" + form.search.data + "%' or" \
                        "categoryproduct.category_product_name LIKE '%" + form.search.data + "%';"
    else:
        product_query = "SELECT " \
                        "t1.id AS product_id, " \
                        "t1.category_product_id AS category_product_id, " \
                        "t1.product_code AS product_code, " \
                        "t1.product_name AS product_name, " \
                        "t1.description AS product_description, " \
                        "t1.price AS product_price, " \
                        "t1.created_at AS product_created_at, " \
                        "t1.created_by AS product_created_by, " \
                        "t1.updated_at AS product_updated_at, " \
                        "t1.updated_by AS product_updated_by, " \
                        "t2.id AS category_product_id, " \
                        "t2.category_product_name AS category_product_name, " \
                        "t2.category_product_description AS category_product_description, " \
                        "t2.created_at AS category_product_created_at, " \
                        "t2.created_by AS category_product_created_by, " \
                        "t2.updated_at AS category_product_updated_at, " \
                        "t2.updated_by AS category_product_updated_by, " \
                        "t4.id AS stock_id, " \
                        "t4.product_id AS stock_product_id, " \
                        "t4.amount AS stock_amount, " \
                        "t4.created_at AS stock_created_at, " \
                        "t4.created_by AS stock_created_by, " \
                        "t4.updated_at AS stock_updated_at, " \
                        "t4.updated_by AS stock_updated_by " \
                        "FROM product AS t1 " \
                        "INNER JOIN categoryproduct AS t2 ON (t2.id = t1.category_product_id) " \
                        "LEFT JOIN stock AS t4 ON (t4.product_id = t1.id);"

        cursor = db.execute_sql(product_query)
        col_names = [col[0] for col in cursor.description]
        product = [dict(zip(col_names, row)) for row in cursor.fetchall()]


    category_product = CategoryProduct.select().execute()

    return render_template('product/list_product.html', current_user=current_user, form=form, len_list=len(product),
                           list_product=product, len_dropdown_category_product=len(category_product),
                           dropdown_category_product=category_product)


# Get Product
@product.route('/getProductByID', methods=['POST'])
@login_required
def functionGetProductByID():
    id = request.form['id']
    # Get User By ID
    product = Product.get_by_id(id)

    product_row = {
        "category_product_id": product.category_product_id,
        "product_code": product.product_code,
        "product_name": product.product_name,
        "description": product.description,
        "price": product.price
    }

    return product_row

# Get Detail Product
@product.route('/getDetailProductByID', methods=['POST'])
@login_required
def functionGetDetailProductByID():
    id = request.form['id']
    print("ID PRODUCT", id)
    # Get User By ID
    # product = Product.get_by_id(id)

    product_query = "SELECT " \
                    "t1.id AS product_id, " \
                    "t1.category_product_id AS category_product_id, " \
                    "t1.product_code AS product_code, " \
                    "t1.product_name AS product_name, " \
                    "t1.description AS product_description, " \
                    "t1.price AS product_price, " \
                    "t1.created_at AS product_created_at, " \
                    "t1.created_by AS product_created_by, " \
                    "t1.updated_at AS product_updated_at, " \
                    "t1.updated_by AS product_updated_by, " \
                    "t2.id AS category_product_id, " \
                    "t2.category_product_name AS category_product_name, " \
                    "t2.category_product_description AS category_product_description, " \
                    "t2.created_at AS category_product_created_at, " \
                    "t2.created_by AS category_product_created_by, " \
                    "t2.updated_at AS category_product_updated_at, " \
                    "t2.updated_by AS category_product_updated_by, " \
                    "t4.id AS stock_id, " \
                    "t4.product_id AS stock_product_id, " \
                    "t4.amount AS stock_amount, " \
                    "t4.created_at AS stock_created_at, " \
                    "t4.created_by AS stock_created_by, " \
                    "t4.updated_at AS stock_updated_at, " \
                    "t4.updated_by AS stock_updated_by " \
                    "FROM product AS t1 " \
                    "INNER JOIN categoryproduct AS t2 ON (t2.id = t1.category_product_id) " \
                    "LEFT JOIN stock AS t4 ON (t4.product_id = t1.id)" \
                    "WHERE t1.id = " + id + ";"

    print("product_query", product_query)

    cursor = db.execute_sql(product_query)
    col_names = [col[0] for col in cursor.description]
    product = [dict(zip(col_names, row)) for row in cursor.fetchall()]

    if product is not None:
        return product[0]
    else:
        print("ERROR")


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
            category_product_id=category_product_id,
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
