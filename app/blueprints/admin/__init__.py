from flask import Blueprint
from flask_login import login_required

from app.functions import __import_all__
from app.models.user import admin_required

bp = Blueprint("admin", __name__)


@bp.before_request
@login_required
@admin_required
def _(): ...


__import_all__("app/blueprints/admin/routes")
