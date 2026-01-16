from flask import render_template

from app.blueprints.admin import bp
from app.models.base import Base


@bp.get("/")
@bp.get("/dashboard")
def dashboard():
    return render_template(
        "admin/pages/dashboard.html",
        title="Dashboard",
        **{cls.__name__: cls for cls in Base.__subclasses__()}
    )
