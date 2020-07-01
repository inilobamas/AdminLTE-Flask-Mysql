from flask import Flask
from flask_login import LoginManager
from conf.config import config
import logging
from logging.config import fileConfig
import os

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
fileConfig('conf/log-app.conf')

def get_logger(name):
    return logging.getLogger(name)


def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    from app.helper import helper as helper_blueprint
    app.register_blueprint(helper_blueprint)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from app.user_account import user_account as user_account_blueprint
    app.register_blueprint(user_account_blueprint)

    from app.category_product import category_product as category_product_blueprint
    app.register_blueprint(category_product_blueprint)

    from app.product_raw import product_raw as product_raw_blueprint
    app.register_blueprint(product_raw_blueprint)

    from app.detail_product_raw import detail_product_raw as detail_product_raw_blueprint
    app.register_blueprint(detail_product_raw_blueprint)

    from app.product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    from app.stock import stock as stock_blueprint
    app.register_blueprint(stock_blueprint)

    from app.detail_stock import detail_stock as detail_stock_blueprint
    app.register_blueprint(detail_stock_blueprint)

    from app.memorandum import memorandum as memorandum_blueprint
    app.register_blueprint(memorandum_blueprint)

    from app.detail_memorandum import detail_memorandum as detail_memorandum_blueprint
    app.register_blueprint(detail_memorandum_blueprint)

    return app
