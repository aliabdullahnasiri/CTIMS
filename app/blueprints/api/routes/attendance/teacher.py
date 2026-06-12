import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.attendance.teacher import AddTeacherAttendanceForm
from app.func import render_td
from app.models.attendance import TeacherAttendance
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID"))),
    (ColumnID("temp_teacher"), ColumnName(g("Teacher"))),
    (ColumnID("date"), ColumnName(g("Date"))),
    (ColumnID("time"), ColumnName(g("Time"))),
    (ColumnID("temp_teacher_attandance_status"), ColumnName(g("Status"))),
]


@bp.get("/fetch/teachers/attendances")
@permission_required(Permission.get("FETCH_TEACHERS_ATTENDANCES"))
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
@permission_required(Permission.get("FETCH_TEACHERS_ATTENDANCES"))
def fetch_teachers_attendances_rows() -> Response:
    teacher_attendances: List[TeacherAttendance] = TeacherAttendance.query.all()

    rows: List[List] = []

    for teacher_attendance in teacher_attendances:
        row = [render_td(col_id, teacher_attendance) for col_id, _ in cols]
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


@bp.get("/fetch/row/teacher/attendance/<string:uid>")
@permission_required(Permission.get("FETCH_TEACHER_ATTENDANCE"))
def fetch_teacher_attendance_row(uid: str) -> Response:
    teacher_attendance: Union[TeacherAttendance, None] = (
        TeacherAttendance.query.filter_by(uid=uid).first()
    )

    if teacher_attendance:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, teacher_attendance) for col_id, _ in cols],
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


@bp.get("/fetch/teacher/attendance/<string:uid>")
@permission_required(Permission.get("FETCH_TEACHER_ATTENDANCE"))
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
                "message": g("Attendance with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/teacher/attendance")
@permission_required(Permission.get("CREATE_TEACHER_ATTENDANCE"))
def add_teacher_attendance() -> Response:
    response: Dict = {}

    form = AddTeacherAttendanceForm()

    if form.validate_on_submit():
        teacher_attendance = TeacherAttendance()

        teacher_attendance.teacher_id = form.teacher_id.data
        teacher_attendance.status = form.status.data

        db.session.add(teacher_attendance)
        db.session.commit()

        response["message"] = g("Teacher attendance added successfully")
        response["title"] = g("Attendance Added")
        response["category"] = "success"
        response["id"] = getattr(teacher_attendance, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )
