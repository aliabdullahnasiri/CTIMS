from flask import render_template

from app.blueprints.admin import bp
from app.forms.job import AddJobForm, UpdateJobForm


@bp.get("/jobs")
def jobs():
    return render_template(
        "admin/pages/jobs.html",
        title="Jobs",
        form={"a": AddJobForm(), "u": UpdateJobForm()},
    )
