from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.forms.subject import AddSubjectForm, UpdateSubjectForm


@bp.get("/subjects")
@login_required
def subjects():
    return render_template(
        "admin/pages/subjects.html",
        title="Subjects",
        form={"a": AddSubjectForm(), "u": UpdateSubjectForm()},
    )
