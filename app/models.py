# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, DateTimeField
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)

# User
class User(UserMixin, BaseModel):
    username = CharField()
    password = CharField()
    fullname = CharField()
    email = CharField(null=True)
    phone = CharField()
    address = CharField(null=True)
    role = CharField()
    status = BooleanField(default=True)
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def generate_password(self, password):
        return generate_password_hash(password)

# Product
class Product(UserMixin, BaseModel):
    product_code = CharField()
    product_name = CharField()
    description = CharField(null=True)
    price = IntegerField(null=True)
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

# Stock
class Stock(UserMixin, BaseModel):
    product_id = CharField()
    amount = IntegerField(null=True)
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

# DetailStock
class DetailStock(UserMixin, BaseModel):
    stock_id = IntegerField()
    user_id = IntegerField() # ini siapa yang urus nota maksudnya
    amount_in = IntegerField() # jika in maka nota pembelian
    amount_out = IntegerField() # jika out maka nota penjualan
    amount_balance = IntegerField()
    start_date = DateTimeField() # kapan dilakukan pembuatan nota
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

# Memorandum
class Memorandum(UserMixin, BaseModel):
    memo_number = CharField()
    memo_date = DateTimeField()
    user_id = IntegerField()
    description = CharField(null=True)
    status = IntegerField() # 1 = pembelian 2 = penjualan
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

# Detail Memorandum
class DetailMemorandum(UserMixin, BaseModel):
    memo_id = IntegerField()
    product_id = IntegerField()
    amount = IntegerField() # 10
    unit = CharField() # kg, liter
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)

# User Account (Kartu Piutang)
class UserAccount(UserMixin, BaseModel):
    user_id = IntegerField()
    memo_id = IntegerField()
    debit = IntegerField(null=True)
    credit = IntegerField(null=True)
    balance = IntegerField(null=True) # not yet paid
    created_at = DateTimeField()
    created_by = IntegerField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)



# Notifier Configuration
class CfgNotify(BaseModel):
    check_order = IntegerField()  # Sort
    notify_type = CharField()  # Notification Type：MAIL/SMS
    notify_name = CharField()  # Notifier Name
    notify_number = CharField()  # Notification Number
    status = BooleanField(default=True)  # Validation Mark


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


# Build Table
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User])


if __name__ == '__main__':
    create_table()
