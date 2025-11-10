from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp


@bp.get("/")
@bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("admin/pages/dashboard.html", title="Dashboard", **globals())
