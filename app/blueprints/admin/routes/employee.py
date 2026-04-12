from flask import render_template

from app.blueprints.admin import bp
from app.forms.employee import AddEmployeeForm, UpdateEmployeeForm


@bp.get("/employees")
def employees():
    return render_template(
        "admin/pages/employees.html",
        title="Employees",
        form={"a": AddEmployeeForm(), "u": UpdateEmployeeForm()},
    )
