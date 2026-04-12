from flask import Blueprint

from app.func import __import_all__

bp = Blueprint("api", __name__)

__import_all__("app/blueprints/api/routes")
__import_all__("app/blueprints/api/routes/attendance")
