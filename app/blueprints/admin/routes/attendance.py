from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp


@bp.get("/teachers/attendances")
@login_required
def teachers_attendances():
    return render_template(
        "admin/pages/teachers-attendances.html",
        title="Teachers Attendances",
    )


@bp.get("/students/attendances")
@login_required
def students_attendances():
    return render_template(
        "admin/pages/students-attendances.html",
        title="Teachers Attendances",
    )
