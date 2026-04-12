from flask import render_template

from app.blueprints.admin import bp
from app.forms.permission import UpdatePermissionForm


@bp.get("/permissions")
def permissions():
    return render_template(
        "admin/pages/permissions.html",
        title="Permissions",
        form={"u": UpdatePermissionForm()},
    )
