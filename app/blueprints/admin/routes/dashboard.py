from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.models.base import Base


@bp.get("/")
@bp.get("/dashboard")
@login_required
def dashboard():
    return render_template(
        "admin/pages/dashboard.html",
        title="Dashboard",
        **{cls.__name__: cls for cls in Base.__subclasses__()}
    )
