from flask import Blueprint, abort
from flask_login import current_user, login_required

from app.func import __import_all__
from app.models.permission import Permission

bp = Blueprint("admin", __name__)


@bp.before_request
@login_required
def _():
    if not current_user.can(Permission.administer()):
        abort(403)


__import_all__("app/blueprints/admin/routes")
