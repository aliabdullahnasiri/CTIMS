from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.forms.attendance.student import AddStudentAttendanceForm
from app.forms.attendance.teacher import AddTeacherAttendanceForm


@bp.get("/teachers/attendances")
@login_required
def teachers_attendances():
    return render_template(
        "admin/pages/attendances/teachers.html",
        title="Teachers Attendances",
        form={"a": AddTeacherAttendanceForm()},
    )


@bp.get("/students/attendances")
@login_required
def students_attendances():
    return render_template(
        "admin/pages/attendances/students.html",
        title="Teachers Attendances",
        form={"a": AddStudentAttendanceForm()},
    )
