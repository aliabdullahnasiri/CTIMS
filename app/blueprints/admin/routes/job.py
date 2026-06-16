from flask import render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.forms.job import AddJobForm, UpdateJobForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/jobs")
@permission_required(Permission.get("FETCH_JOBS") | Permission.get("FETCH_JOB"))
def jobs():
    return render_template(
        "admin/pages/jobs.html",
        title=_("JOBS_LABEL"),
        form={"a": AddJobForm(), "u": UpdateJobForm()},
    )
