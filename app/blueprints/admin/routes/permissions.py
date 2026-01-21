from flask import render_template

from app.blueprints.admin import bp


@bp.get("/permissions")
def permissions():
    return render_template(
        "admin/pages/permissions.html",
        title="Permissions",
    )
