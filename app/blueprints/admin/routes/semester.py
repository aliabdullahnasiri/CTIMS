from flask import render_template

from app.blueprints.admin import bp
from app.forms.semester import AddSemesterForm, UpdateSemesterForm


@bp.get("/semesters")
def semesters():
    return render_template(
        "admin/pages/semesters.html",
        title="Semesters",
        form={"a": AddSemesterForm(), "u": UpdateSemesterForm()},
    )
