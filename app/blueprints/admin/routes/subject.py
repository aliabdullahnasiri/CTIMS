from flask import render_template

from app.blueprints.admin import bp
from app.forms.subject import AddSubjectForm, UpdateSubjectForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/subjects")
@permission_required(Permission.get("FETCH_SUBJECTS") | Permission.get("FETCH_SUBJECT"))
def subjects():
    return render_template(
        "admin/pages/subjects.html",
        title="Subjects",
        form={"a": AddSubjectForm(), "u": UpdateSubjectForm()},
    )
