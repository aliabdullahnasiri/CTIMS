from flask import render_template

from app.blueprints.admin import bp
from app.forms.result import AddResultForm, UpdateResultForm


@bp.get("/results")
def results():
    return render_template(
        "admin/pages/results.html",
        title="Results",
        form={"a": AddResultForm(), "u": UpdateResultForm()},
    )
