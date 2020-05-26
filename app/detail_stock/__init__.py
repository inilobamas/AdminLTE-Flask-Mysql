from flask import Blueprint

detail_stock = Blueprint('detail_stock', __name__)

from . import views, forms
