from flask import render_template

from app.blueprints.admin import bp
from app.models.base import Base
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/")
@bp.get("/dashboard")
@permission_required(Permission.get("VIEW_DASHBOARD"))
def dashboard():
    return render_template(
        "admin/pages/dashboard.html",
        title="Dashboard",
        **{cls.__name__: cls for cls in Base.__subclasses__()}
    )
