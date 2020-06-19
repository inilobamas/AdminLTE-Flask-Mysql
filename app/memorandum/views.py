from flask import render_template, redirect, request, url_for, flash
from . import memorandum
from .forms import SearchForm
from app.models import Memorandum, User, CategoryProduct, Product
from flask_login import login_required, current_user
from peewee import MySQLDatabase, JOIN
from conf.config import config
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
        memorandum = Memorandum.select(Memorandum, User).join(User, on=(User.id == Memorandum.user_id)).execute()

    return render_template('memorandum/list_memorandum.html', current_user=current_user, form=form, len_list=len(memorandum), list_memorandum=memorandum)

# Add Memorandum
@memorandum.route('/add_memorandum', methods=['GET', 'POST'])
@login_required
def functionAddMemorandum():
    form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     user = User.select()\
    #         .where(
    #             User.username.contains(form.search.data)
    #             | User.fullname.contains(form.search.data)
    #             | User.email.contains(form.search.data)
    #             | User.address.contains(form.search.data)
    #             | User.phone.contains(form.search.data)
    #             | User.role.contains(form.search.data)
    #         )
    # else:
    #     user = User.select().execute()

    user = User.select().execute()
    # category_product = CategoryProduct.select().execute()
    # product = Product.select().execute()
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

    return render_template('memorandum/add_memorandum.html', current_user=current_user, form=form, len_list_user=len(user), list_user=user, len_product=len(product), list_product=product)

# Add Memorandum
@memorandum.route('/add_memorandum2', methods=['GET', 'POST'])
@login_required
def functionAddMemorandum2():
    form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     user = User.select()\
    #         .where(
    #             User.username.contains(form.search.data)
    #             | User.fullname.contains(form.search.data)
    #             | User.email.contains(form.search.data)
    #             | User.address.contains(form.search.data)
    #             | User.phone.contains(form.search.data)
    #             | User.role.contains(form.search.data)
    #         )
    # else:
    #     user = User.select().execute()

    return render_template('memorandum/add_memorandum2.html', current_user=current_user, form=form) #, len_list=len(product), list_user=user)