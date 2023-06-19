from flask import Blueprint

sales = Blueprint("sales", __name__)

from . import views