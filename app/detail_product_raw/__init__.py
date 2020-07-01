from flask import Blueprint

detail_product_raw = Blueprint('detail_product_raw', __name__)

from . import views, forms
