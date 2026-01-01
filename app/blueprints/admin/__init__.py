from flask import Blueprint

from app.functions import __import_all__

bp = Blueprint("admin", __name__)

__import_all__("app/blueprints/admin/routes")
