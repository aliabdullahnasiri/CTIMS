from flask import render_template

from app.blueprints.admin import bp
from app.forms.job import AddJobForm, UpdateJobForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/jobs")
@permission_required(Permission.get("FETCH_JOBS") | Permission.get("FETCH_JOB"))
def jobs():
    return render_template(
        "admin/pages/jobs.html",
        title="Jobs",
        form={"a": AddJobForm(), "u": UpdateJobForm()},
    )
