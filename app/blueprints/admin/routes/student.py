from flask import render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.forms.student import AddStudentForm, UpdateStudentForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/students")
@permission_required(Permission.get("FETCH_USERS") | Permission.get("FETCH_USER"))
def students():
    return render_template(
        "admin/pages/students.html",
        title=_("STUDENTS_LABEL"),
        form={"a": AddStudentForm(), "u": UpdateStudentForm()},
    )
