import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.attendance.student import AddStudentAttendanceForm
from app.functions import render_td
from app.models.attendance import StudentAttendance
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_student"), ColumnName("Student")),
    (ColumnID("date"), ColumnName("Date")),
    (ColumnID("time"), ColumnName("Time")),
    (ColumnID("temp_student_attandance_status"), ColumnName("Status")),
]


@bp.get("/fetch/students/attendances")
@login_required
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
@login_required
def fetch_students_attendances_rows() -> Response:
    student_attendances: List[StudentAttendance] = StudentAttendance.query.all()

    rows: List[List] = []

    for sa in student_attendances:
        row = [render_td(col_id, sa) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/student/attendance/<string:uid>")
@login_required
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
                "message": "Attendance with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/student/attendance/<string:uid>")
@login_required
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
                "message": "Attendance with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/student/attendance")
@login_required
def add_student_attendance() -> Response:
    response: Dict = {}

    form = AddStudentAttendanceForm()

    if form.validate_on_submit():
        student_attendance = StudentAttendance()

        student_attendance.student_id = form.student_id.data
        student_attendance.status = form.status.data

        db.session.add(student_attendance)
        db.session.commit()

        response["message"] = "Student attendance added successfully"
        response["category"] = "success"
        response["title"] = "Attendance Added"
        response["id"] = student_attendance.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )
