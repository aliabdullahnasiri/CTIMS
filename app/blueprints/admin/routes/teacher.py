from flask import render_template

from app.blueprints.admin import bp
from app.forms.teacher import AddTeacherForm, UpdateTeacherForm


@bp.get("/teachers")
def teachers():
    return render_template(
        "admin/pages/teachers.html",
        title="Teachers",
        form={"a": AddTeacherForm(), "u": UpdateTeacherForm()},
    )
