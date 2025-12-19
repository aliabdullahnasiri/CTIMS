import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.attendance.teacher import AddTeacherAttendanceForm
from app.models.attendance import TeacherAttendance
from app.types import ColumnID, ColumnName


@bp.get("/fetch/teachers/attendances")
@login_required
def fetch_teachers_attendances() -> Response:
    teacher_attendances: List[Dict] = [
        teacher_attendance.to_dict()
        for teacher_attendance in TeacherAttendance.query.all()
    ]

    return Response(
        json.dumps(teacher_attendances),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/teachers/attendances")
@login_required
def fetch_teachers_attendances_rows() -> Response:
    teacher_attendances: List[TeacherAttendance] = TeacherAttendance.query.all()

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("UID")),
    ]

    rows: List[List] = []

    for teacher_attendance in teacher_attendances:
        dct = teacher_attendance.to_dict()
        row = [dct.get(col_id, "N/A") for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/teacher/attendance/<string:uid>")
@login_required
def fetch_teacher_attendance_row(uid: str) -> Response:
    teacher_attendance: Union[TeacherAttendance, None] = (
        TeacherAttendance.query.filter_by(uid=uid).first()
    )

    if teacher_attendance:
        return Response(
            json.dumps(teacher_attendance.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Attendance with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/teacher/attendance/<string:uid>")
@login_required
def fetch_teacher_attendance(uid: str) -> Response:
    teacher_attendance: Union[TeacherAttendance, None] = (
        TeacherAttendance.query.filter_by(uid=uid).first()
    )

    if teacher_attendance:
        return Response(
            json.dumps(teacher_attendance.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Attendance with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/teacher/attendance")
@login_required
def add_teacher_attendance() -> Response:
    response: Dict = {}

    form = AddTeacherAttendanceForm()

    if form.validate_on_submit():
        teacher_attendance = TeacherAttendance()

        teacher_attendance.teacher_id = form.teacher_id.data
        teacher_attendance.status = form.status.data

        db.session.add(teacher_attendance)
        db.session.commit()

        response["message"] = "Teacher attendance added successfully"
        response["category"] = "success"
        response["title"] = "Attendance Added"
        response["id"] = teacher_attendance.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )
