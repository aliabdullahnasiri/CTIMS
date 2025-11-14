from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.forms.semester import AddSemesterForm, UpdateSemesterForm


@bp.get("/semesters")
@login_required
def semesters():
    return render_template(
        "admin/pages/semesters.html",
        title="Semesters",
        form={"a": AddSemesterForm(), "u": UpdateSemesterForm()},
    )
