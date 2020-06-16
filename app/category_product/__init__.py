from flask import Blueprint

category_product = Blueprint('category_product', __name__)

from . import views, forms
