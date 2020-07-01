from flask import render_template, redirect, request, url_for, flash
from . import product_raw
from .forms import SearchForm
from app.models import ProductRaw, User, Stock, DetailStock, DetailProductRaw
from flask_login import login_required, current_user
from datetime import datetime, date
from peewee import MySQLDatabase, JOIN
from conf.config import config
import json, datetime, os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)

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

# Add Product Row - Restock
@product_raw.route('/product_raw_restock', methods=['GET', 'POST'])
@login_required
def functionProductRawRestock():
    form = SearchForm()
    product_raw_id = request.args.get('id')

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

    timeNow = datetime.datetime.now()
    memorandumCode = 0
    print("product_raw_id", product_raw_id)
    productRaw = ProductRaw.get_by_id(product_raw_id)
    print(str(productRaw.id))

    return render_template('product_raw/add_product_raw_restock.html', current_user=current_user, form=form, len_product=len(product), list_product=product, timeNow=timeNow, memorandumCode=memorandumCode, productRaw=productRaw)

# Insert Product (with modal)
@product_raw.route('/insertDetailProductRaw', methods=['POST'])
@login_required
def functionInsertDetailProductRaw():
    form = SearchForm()
    row = {
        "status": "failed",
        "message": "failed"
    }

    data = request.get_json()
    product_raw_id = data['productRawID']
    productRawDescription = data['productRawDescription']
    detailMemorandum = data['detailMemorandum']

    if detailMemorandum:
        try:
            for row in detailMemorandum:
                # Get Stock by product id
                stock_id = 0
                stock_amount = 0
                stock = Stock.select().where(Stock.product_id == row['product_id'])
                if stock:
                    try:
                        stock_id = stock[0].id
                        stock_amount = int(row['amount']) + stock[0].amount

                        # Update Amount Stock + detailMemorandum['amount'] where product_id
                        query_stock_update = Stock.update(
                            amount=stock_amount,
                            updated_by=current_user.id,
                            updated_at=datetime.datetime.now()
                        )
                        query_stock_update.where(Stock.id == stock_id).execute()
                    except Exception as e:
                        print("Stock Update Failed", e)
                        row['status'] = "danger"
                        row['message'] = "Failed to Update Stock"
                        return row
                else:
                    print("MASUK ELSE")
                    try:
                        stock_amount = int(row['amount'])

                        # Insert Amount Stock + detailMemorandum['amount'] where product_id
                        query_stock_insert = Stock.insert(
                            product_id=row['product_id'],
                            amount=stock_amount,
                            created_by=current_user.id,
                            created_at=datetime.datetime.now()
                        ).execute()
                        print("query_stock_insert", query_stock_insert)
                        stock_id = query_stock_insert
                    except Exception as e:
                        print("Stock Update Failed", e)
                        row['status'] = "danger"
                        row['message'] = "Failed to Update Stock"
                        return row

                print("stock_id", stock_id)
                try:
                    # DetailStock, stock_id, user_id amount_in+ amount_balance+
                    DetailStock.insert(
                        stock_id=stock_id,
                        user_id=current_user.id,
                        amount_in=int(row['amount']),
                        amount_out=0,
                        amount_balance=stock_amount,
                        start_date=datetime.datetime.now(),
                        created_by=current_user.id,
                        created_at=datetime.datetime.now()
                    ).execute()
                except Exception as e:
                    print("DetailStock Insert Failed", e)
                    row['status'] = "danger"
                    row['message'] = "Failed to Insert Detail Stock"
                    return row

                try:
                    # DetailProductRaw, product_raw_id product_id description amount
                    DetailProductRaw.insert(
                        product_raw_id=product_raw_id,
                        product_id=row['product_id'],
                        description=productRawDescription,
                        amount=row['amount'],
                        created_by=current_user.id,
                        created_at=datetime.datetime.now()
                    ).execute()

                    row['status'] = "success"
                    row['message'] = "Successfully Inserted"
                except Exception as e:
                    print("DetailStockRaw Insert Failed", e)
                    row['status'] = "danger"
                    row['message'] = "Failed to Insert Detail Product Raw"

        except Exception as e:
            print("Insert Failed", e)
            row['status'] = "danger"
            row['message'] = "Failed to Insert"
            return row

    return row