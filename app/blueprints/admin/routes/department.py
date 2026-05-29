from flask import render_template

from app.blueprints.admin import bp
from app.forms.department import AddDepartmentForm, UpdateDepartmentForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/departments")
@permission_required(
    Permission.get("FETCH_DEPARTMENTS") | Permission.get("FETCH_DEPARTMENT")
)
def departments():
    return render_template(
        "admin/pages/departments.html",
        title="Departments",
        form={"a": AddDepartmentForm(), "u": UpdateDepartmentForm()},
    )
