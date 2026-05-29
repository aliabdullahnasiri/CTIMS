from flask import render_template

from app.blueprints.admin import bp
from app.forms.exam import AddExamForm, UpdateExamForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/exams")
@permission_required(Permission.get("FETCH_EXAMS") | Permission.get("FETCH_EXAM"))
def exams():
    return render_template(
        "admin/pages/exams.html",
        title="Exams",
        form={"a": AddExamForm(), "u": UpdateExamForm()},
    )
