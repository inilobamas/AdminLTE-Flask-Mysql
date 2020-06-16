from flask import Blueprint

product_raw = Blueprint('product_raw', __name__)

from . import views, forms
