from flask import render_template, redirect, request, url_for, flash
from . import memorandum
from .forms import SearchForm
from app.models import Memorandum, User, CategoryProduct, Product, DetailMemorandum, UserAccount, Stock, DetailStock
from flask_login import login_required, current_user
from peewee import MySQLDatabase, JOIN
from conf.config import config
from datetime import datetime, date
from ..helper.views import formatrupiah
import json, datetime, os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)

# List Memorandum
@memorandum.route('/memorandum', methods=['GET', 'POST'])
@login_required
def functionGetMemorandum():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        memorandum = Memorandum.select(Memorandum, User) \
            .join(User, on=(User.id == Memorandum.user_id)) \
            .where(
                Memorandum.memo_number.contains(form.search.data)
                | Memorandum.description.contains(form.search.data)
                | User.fullname.contains(form.search.data)
            )
    else:
        memorandum = Memorandum.select(Memorandum, User).join(User, on=(User.id == Memorandum.user_id))

    for row in memorandum:
        row.total_price = formatrupiah(row.total_price)

    return render_template('memorandum/list_memorandum.html', current_user=current_user, form=form, len_list=len(memorandum), list_memorandum=memorandum)

# Get Latest Memorandum Code
def functionGetMemorandumCode():
    # Get User By ID
    memorandum = Memorandum.select().order_by(Memorandum.id.desc()).first()

    memorandum_code = "1"
    if memorandum != None:
        memorandum_code = str(memorandum.id + 1)

    product_code = "NJL-" + memorandum_code.zfill(6) # NBL = Nota Beli NJL = Nota Jual NPP = Nota Pelunasan Pembayaran
    return product_code

# Add Memorandum
@memorandum.route('/add_memorandum', methods=['GET', 'POST'])
@login_required
def functionAddMemorandum():
    form = SearchForm()

    user = User.select().execute()
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

    timeNow = str(date.today())
    memorandumCode = functionGetMemorandumCode()

    return render_template('memorandum/add_memorandum.html', current_user=current_user, form=form, len_list_user=len(user), list_user=user, len_product=len(product), list_product=product, timeNow=timeNow, memorandumCode=memorandumCode)

# Insert Product (with modal)
@memorandum.route('/insertMemorandumAndDetailMemorandum', methods=['POST'])
@login_required
def functionInsertMemorandumAndDetailMemorandum():
    form = SearchForm()
    row = {
        "status": "success",
        "message": "Success"
    }

    data = request.get_json()
    data_user_id = data['user_id']
    detailMemorandum = data['detailMemorandum']
    memorandumCode = functionGetMemorandumCode()

    if detailMemorandum:
        try:
            print("data['status']", data['status'] == 1)
            status_memo = False
            if data['status'] == 1:
                status_memo = True
            else:
                data['total_remaining'] = data['total_price']

            result_memorandum = Memorandum.insert(
                memo_number=memorandumCode,
                memo_date=datetime.datetime.now(),
                memo_end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                user_id=data_user_id,
                description=data['description'],
                total_amount=data['total_amount'],
                total_price=data['total_price'],
                total_remaining=data['total_remaining'],
                status=data['status'],
                created_by=current_user.id,
                created_at=datetime.datetime.now()
            ).execute()

            try:
                if status_memo:
                    UserAccount.insert(
                        user_id=data_user_id,
                        memo_id=result_memorandum,
                        debit=0,
                        credit=0,
                        balance=0,
                        created_by=current_user.id,
                        created_at=datetime.datetime.now()
                    ).execute()
                else:
                    UserAccount.insert(
                        user_id=data_user_id,
                        memo_id=result_memorandum,
                        debit=0,
                        credit=data['total_price'],
                        balance=data['total_remaining'],
                        created_by=current_user.id,
                        created_at=datetime.datetime.now()
                    ).execute()
            except Exception as e:
                row['status'] = "danger"
                row['message'] = "Failed to Insert User Account"
                return row

            for data in detailMemorandum:
                DetailMemorandum.insert(
                    memo_id=result_memorandum,
                    product_id=data['product_id'],
                    amount=data['amount'],
                    unit="kg",
                    created_by=current_user.id,
                    created_at=datetime.datetime.now()
                ).execute()

                try:
                    stock = Stock.select().where(Stock.product_id == data['product_id'])
                    amount_remaining = stock[0].amount - int(data['amount'])

                    query_stock_update = Stock.update(
                        amount=amount_remaining,
                        updated_by=current_user.id,
                        updated_at=datetime.datetime.now()
                    )
                    query_stock_update.where(Stock.product_id == data['product_id']).execute()
                except Exception as e:
                    print("Except Update Stock", e)
                    row['status'] = "danger"
                    row['message'] = "Failed to Update Stock"
                    return row

                try:
                    DetailStock.insert(
                        stock_id=stock[0].id,
                        user_id=data_user_id,
                        amount_in=0,
                        amount_out=data['amount'],
                        amount_balance=amount_remaining,
                        start_date=datetime.datetime.now(),
                        created_at=datetime.datetime.now(),
                        created_by=current_user.id
                    ).execute()
                except Exception as e:
                    print("Except Insert Detail Stock", e)
                    row['status'] = "danger"
                    row['message'] = "Failed to Insert Detail Stock"
                    return row

            row['status'] = "success"
            row['message'] = "Successfully Inserted"
        except Exception as e:
            print("Except", e)
            row['status'] = "danger"
            row['message'] = "Failed to Insert"
    else:
        row['status'] = "danger"
        row['message'] = "There's No Data"

    return row

# List Memorandum
@memorandum.route('/detail_memorandum', methods=['GET', 'POST'])
@login_required
def functionGetDetailMemorandum():
    form = SearchForm()
    memo_id = request.args.get('id')

    memorandum = Memorandum.get_by_id(memo_id)
    detail_memorandum = DetailMemorandum.select(Product, DetailMemorandum, (DetailMemorandum.amount * Product.price).alias('detail_total')) \
        .join(Product, on=(Product.id == DetailMemorandum.product_id)) \
        .where(DetailMemorandum.memo_id == memo_id)

    user = User.get_by_id(memorandum.user_id)

    for row in detail_memorandum:
        row.product.price = formatrupiah(row.product.price)
        row.detail_total = formatrupiah(row.detail_total)

    memorandum.total_price = formatrupiah(memorandum.total_price)

    return render_template('detail_memorandum/list_detail_memorandum.html', current_user=current_user, form=form, memorandum=memorandum, len_detail_memorandum=len(detail_memorandum), detail_memorandum=detail_memorandum, user=user)