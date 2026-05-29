from flask import Blueprint
from flask_login import current_user

from app.blueprints.api.routes.navbar import build_navbar
from app.func import __import_all__

bp = Blueprint("admin", __name__)


@bp.context_processor
def _():
    return {"navbar": build_navbar(current_user)}


__import_all__("app/blueprints/admin/routes")
