from flask import render_template

from app.blueprints.admin import bp
from app.forms.student import AddStudentForm, UpdateStudentForm


@bp.get("/students")
def students():
    return render_template(
        "admin/pages/students.html",
        title="Students",
        form={"a": AddStudentForm(), "u": UpdateStudentForm()},
    )
