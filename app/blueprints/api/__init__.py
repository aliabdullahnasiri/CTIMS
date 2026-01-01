from flask import Blueprint

from app.functions import __import_all__

bp = Blueprint("api", __name__)

__import_all__("app/blueprints/api/routes")
