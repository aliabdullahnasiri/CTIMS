from flask import render_template

from app.blueprints.admin import bp
from app.forms.department import AddDepartmentForm, UpdateDepartmentForm


@bp.get("/departments")
def departments():
    return render_template(
        "admin/pages/departments.html",
        title="Departments",
        form={"a": AddDepartmentForm(), "u": UpdateDepartmentForm()},
    )
