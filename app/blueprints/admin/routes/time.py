from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.forms.time import AddTimeForm, UpdateTimeForm


@bp.get("/times")
@login_required
def times():
    return render_template(
        "admin/pages/times.html",
        title="Times",
        form={"a": AddTimeForm(), "u": UpdateTimeForm()},
    )
