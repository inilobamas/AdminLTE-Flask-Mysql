from flask import Blueprint

detail_memorandum = Blueprint('detail_memorandum', __name__)

from . import views, forms
