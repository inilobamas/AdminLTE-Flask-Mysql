from flask import Blueprint

stock = Blueprint('stock', __name__)

from . import views, forms
