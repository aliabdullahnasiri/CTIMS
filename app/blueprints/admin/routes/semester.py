from flask import render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.forms.semester import AddSemesterForm, UpdateSemesterForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/semesters")
@permission_required(
    Permission.get("FETCH_SEMESTERS") | Permission.get("FETCH_SEMESTER")
)
def semesters():
    return render_template(
        "admin/pages/semesters.html",
        title=_("Semesters"),
        form={"a": AddSemesterForm(), "u": UpdateSemesterForm()},
    )
