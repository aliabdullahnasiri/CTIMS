from flask import render_template

from app.blueprints.admin import bp
from app.forms.role import AddRoleForm, UpdateRoleForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/roles")
@permission_required(Permission.get("FETCH_ROLES") | Permission.get("FETCH_ROLE"))
def roles():
    return render_template(
        "admin/pages/roles.html",
        title="Roles",
        form={"a": AddRoleForm(), "u": UpdateRoleForm()},
    )
