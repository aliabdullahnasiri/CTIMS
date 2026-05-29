from flask import render_template

from app.blueprints.admin import bp
from app.forms.attendance.student import AddStudentAttendanceForm
from app.forms.attendance.teacher import AddTeacherAttendanceForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/teachers/attendances")
@permission_required(
    Permission.get("FETCH_TEACHERS_ATTENDANCES")
    | Permission.get("FETCH_TEACHER_ATTENDANCE")
)
def teachers_attendances():
    return render_template(
        "admin/pages/attendances/teachers.html",
        title="Teachers Attendances",
        form={"a": AddTeacherAttendanceForm()},
    )


@bp.get("/students/attendances")
@permission_required(
    Permission.get("FETCH_STUDENTS_ATTENDANCES")
    | Permission.get("FETCH_STUDENT_ATTENDANCE")
)
def students_attendances():
    return render_template(
        "admin/pages/attendances/students.html",
        title="Students Attendances",
        form={"a": AddStudentAttendanceForm()},
    )
