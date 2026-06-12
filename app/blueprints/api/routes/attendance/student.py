import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.attendance.student import AddStudentAttendanceForm
from app.func import render_td
from app.models.attendance import StudentAttendance
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID"))),
    (ColumnID("temp_student"), ColumnName(g("Student"))),
    (ColumnID("date"), ColumnName(g("Date"))),
    (ColumnID("time"), ColumnName(g("Time"))),
    (ColumnID("temp_student_attandance_status"), ColumnName(g("Status"))),
]


@bp.get("/fetch/students/attendances")
@permission_required(Permission.get("FETCH_STUDENTS_ATTENDANCES"))
def fetch_students_attendances() -> Response:
    student_attendances: List[Dict] = [
        student_attendance.to_dict()
        for student_attendance in StudentAttendance.query.all()
    ]

    return Response(
        json.dumps(student_attendances),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/students/attendances")
@permission_required(Permission.get("FETCH_STUDENTS_ATTENDANCES"))
def fetch_students_attendances_rows() -> Response:
    student_attendances: List[StudentAttendance] = StudentAttendance.query.all()

    rows: List[List] = []

    for sa in student_attendances:
        row = [render_td(col_id, sa) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": [(col_id, g(col_name)) for col_id, col_name in cols],
        "rows": rows,
    }

    return Response(
        json.dumps(dct),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/student/attendance/<string:uid>")
@permission_required(Permission.get("FETCH_STUDENT_ATTENDANCE"))
def fetch_student_attendance_row(uid: str) -> Response:
    sa: Union[StudentAttendance, None] = StudentAttendance.query.filter_by(
        uid=uid
    ).first()

    if sa:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, sa) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("Attendance with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/student/attendance/<string:uid>")
@permission_required(Permission.get("FETCH_STUDENT_ATTENDANCE"))
def fetch_student_attendance(uid: str) -> Response:
    student_attendance: Union[StudentAttendance, None] = (
        StudentAttendance.query.filter_by(uid=uid).first()
    )

    if student_attendance:
        return Response(
            json.dumps(student_attendance.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("Attendance with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/student/attendance")
@permission_required(Permission.get("FETCH_STUDENT_ATTENDANCES"))
def add_student_attendance() -> Response:
    response: Dict = {}

    form = AddStudentAttendanceForm()

    if form.validate_on_submit():
        student_attendance = StudentAttendance()

        student_attendance.student_id = form.student_id.data
        student_attendance.status = form.status.data

        db.session.add(student_attendance)
        db.session.commit()

        response["message"] = g("Student attendance added successfully")
        response["title"] = g("Attendance Added")
        response["category"] = "success"
        response["id"] = getattr(student_attendance, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )
