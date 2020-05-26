from flask import Blueprint

memorandum = Blueprint('memorandum', __name__)

from . import views, forms
