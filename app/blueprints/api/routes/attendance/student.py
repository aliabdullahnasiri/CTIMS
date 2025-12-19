import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.attendance.student import AddStudentAttendanceForm
from app.models.attendance import StudentAttendance
from app.types import ColumnID, ColumnName


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

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("UID")),
    ]

    rows: List[List] = []

    for student_attendance in student_attendances:
        dct = student_attendance.to_dict()
        row = [dct.get(col_id, "N/A") for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/student/attendance/<string:uid>")
@login_required
def fetch_student_attendance_row(uid: str) -> Response:
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
