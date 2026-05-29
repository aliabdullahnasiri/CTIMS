from flask import render_template

from app.blueprints.admin import bp
from app.forms.employee import AddEmployeeForm, UpdateEmployeeForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/employees")
@permission_required(
    Permission.get("FETCH_EMPLOYEES") | Permission.get("FETCH_EMPLOYEE")
)
def employees():
    return render_template(
        "admin/pages/employees.html",
        title="Employees",
        form={"a": AddEmployeeForm(), "u": UpdateEmployeeForm()},
    )
