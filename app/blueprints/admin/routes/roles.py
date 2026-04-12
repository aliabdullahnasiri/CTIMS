from flask import render_template

from app.blueprints.admin import bp
from app.forms.role import UpdateRoleForm


@bp.get("/roles")
def roles():
    return render_template(
        "admin/pages/roles.html",
        title="Roles",
        form={"u": UpdateRoleForm()},
    )
