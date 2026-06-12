from flask import render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.forms.result import AddResultForm, UpdateResultForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/results")
@permission_required(Permission.get("FETCH_RESULTS") | Permission.get("FETCH_RESULT"))
def results():
    return render_template(
        "admin/pages/results.html",
        title=_("Results"),
        form={"a": AddResultForm(), "u": UpdateResultForm()},
    )
