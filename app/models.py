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
class Product(BaseModel):
    product_code = CharField()
    product_name = CharField()
    description = CharField(null=True)
    price = IntegerField(null=True)
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
