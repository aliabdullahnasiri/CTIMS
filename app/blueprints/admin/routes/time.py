from flask import render_template

from app.blueprints.admin import bp
from app.forms.time import AddTimeForm, UpdateTimeForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/times")
@permission_required(Permission.get("FETCH_TIMES") | Permission.get("FETCH_TIME"))
def times():
    return render_template(
        "admin/pages/times.html",
        title="Times",
        form={"a": AddTimeForm(), "u": UpdateTimeForm()},
    )
