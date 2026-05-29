from flask import render_template

from app.blueprints.admin import bp
from app.forms.permission import UpdatePermissionForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/permissions")
@permission_required(
    Permission.get("FETCH_PERMISSIONS") | Permission.get("FETCH_PERMISSION")
)
def permissions():
    return render_template(
        "admin/pages/permissions.html",
        title="Permissions",
        form={"u": UpdatePermissionForm()},
    )
