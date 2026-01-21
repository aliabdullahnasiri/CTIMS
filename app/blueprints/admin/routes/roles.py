from flask import render_template

from app.blueprints.admin import bp


@bp.get("/roles")
def roles():
    return render_template(
        "admin/pages/roles.html",
        title="Roles",
    )
