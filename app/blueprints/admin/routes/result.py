from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.forms.result import AddResultForm, UpdateResultForm


@bp.get("/results")
@login_required
def results():
    return render_template(
        "admin/pages/results.html",
        title="Results",
        form={"a": AddResultForm(), "u": UpdateResultForm()},
    )
