from flask import render_template

from app.blueprints.admin import bp
from app.forms.exam import AddExamForm, UpdateExamForm


@bp.get("/exams")
def exams():
    return render_template(
        "admin/pages/exams.html",
        title="Exams",
        form={"a": AddExamForm(), "u": UpdateExamForm()},
    )
