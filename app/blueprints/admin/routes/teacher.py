from flask import render_template

from app.blueprints.admin import bp
from app.forms.teacher import AddTeacherForm, UpdateTeacherForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/teachers")
@permission_required(Permission.get("FETCH_TEACHERS") | Permission.get("FETCH_TEACHER"))
def teachers():
    return render_template(
        "admin/pages/teachers.html",
        title="Teachers",
        form={"a": AddTeacherForm(), "u": UpdateTeacherForm()},
    )
