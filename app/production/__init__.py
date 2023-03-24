from flask import Blueprint

production = Blueprint("production", __name__)

from . import views