from flask import render_template, redirect, request, url_for, flash
from . import user_account
from .forms import SearchForm
from app.models import UserAccount, Memorandum, User
from flask_login import login_required, current_user
from ..helper.views import formatrupiah
from datetime import date
import json, datetime

# List User Account
@user_account.route('/user_account', methods=['GET', 'POST'])
@login_required
def functionGetUserAccount():
    form = SearchForm()
    user_id = request.args.get('id')
    if request.method == 'POST' and form.validate_on_submit():
        user_account = UserAccount.select(UserAccount, Memorandum) \
            .join(Memorandum, on=(Memorandum.id == UserAccount.memo_id)) \
            .where(Memorandum.user_id == user_id
                   & (Memorandum.memo_number.contains(form.search.data)
                   | Memorandum.description.contains(form.search.data))
                   )
    else:
        user_account = UserAccount.select(UserAccount, Memorandum)\
            .join(Memorandum, on=(Memorandum.id == UserAccount.memo_id))\
            .where(Memorandum.user_id == user_id)

    total_credit_memorandum = 0
    total_remaining_memorandum = 0
    list_days_left = []
    for row in user_account:
        total_credit_memorandum = total_credit_memorandum + row.credit
        total_remaining_memorandum = total_remaining_memorandum + row.balance
        row.debit = formatrupiah(row.debit)
        row.credit = formatrupiah(row.credit)
        row.balance = formatrupiah(row.balance)

        days_left = 0
        if row.memorandum.memo_end_date.date() > datetime.datetime.now().date():
            delta = row.memorandum.memo_end_date.date() - datetime.datetime.now().date()
            days_left = str(delta.days)
        else:
            days_left = "Expired"

        list_days_left.append({"days_left":days_left})

    user = User.get_by_id(user_id)
    total_credit_memorandum = formatrupiah(total_credit_memorandum)
    total_remaining_memorandum = formatrupiah(total_remaining_memorandum)

    return render_template('user_account/list_user_account.html', total_credit_memorandum=total_credit_memorandum, total_remaining_memorandum=total_remaining_memorandum, current_user=current_user, form=form, len_user_account=len(user_account), list_user_account=user_account, user=user, list_days_left=list_days_left)

# Add User Account
@user_account.route('/add_user_account', methods=['GET', 'POST'])
@login_required
def functionAddUserAccount():
    form = SearchForm()
    user_id = request.args.get('id')

    user = User.get_by_id(user_id)
    user_account_code = functionGetUserAccountCode()

    memorandum = Memorandum.select().where(Memorandum.user_id == user_id and Memorandum.status == 2)

    total_memorandum_price = 0
    sisa_memorandum = 0

    for row in memorandum:
        total_memorandum_price = total_memorandum_price + row.total_price
        if row.status == 2:
            sisa_memorandum = sisa_memorandum + row.total_price

        row.total_price = formatrupiah(row.total_price)

    string_total_memorandum_price = formatrupiah(total_memorandum_price)
    string_sisa_memorandum = formatrupiah(sisa_memorandum)

    return render_template('user_account/add_user_account.html', current_user=current_user, form=form, user=user, user_account_code=user_account_code, len_list_memorandum=len(memorandum), list_memorandum=memorandum, total_memorandum_price=string_total_memorandum_price, sisa_memorandum=string_sisa_memorandum)

# Get Latest User Account Code
def functionGetUserAccountCode():
    # Get User By ID
    user_account = UserAccount.select().order_by(UserAccount.id.desc()).first()

    user_account_code = "1"
    if user_account != None:
        user_account_code = str(user_account.id + 1)

    product_code = "NPP-" + user_account_code.zfill(6) # NBL = Nota Beli NJL = Nota Jual NPP = Nota Pelunasan Pembayaran
    return product_code