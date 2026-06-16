import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.semester import AddSemesterForm, UpdateSemesterForm
from app.func import render_td
from app.models.permission import Permission
from app.models.semester import Semester
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("name"), ColumnName(g("NAME_LABEL"))),
    (ColumnID("number"), ColumnName(g("NUMBER_LABEL"))),
]


@bp.get("/fetch/semesters")
@permission_required(Permission.get("FETCH_SEMESTERS"))
def fetch_semesters() -> Response:
    semesters: List[Dict] = [semester.to_dict() for semester in Semester.query.all()]

    return Response(
        json.dumps(semesters),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/semesters")
@permission_required(Permission.get("FETCH_SEMESTERS"))
def fetch_semesters_rows() -> Response:
    semesters: List[Semester] = Semester.query.all()

    rows: List[List] = []

    for semester in semesters:
        row = [render_td(col_id, semester) for col_id, _ in cols]
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


@bp.get("/fetch/row/semester/<string:uid>")
@permission_required(Permission.get("FETCH_SEMESTER"))
def fetch_semester_row(uid: str) -> Response:
    semester: Union[Semester, None] = Semester.query.filter_by(uid=uid).first()

    if semester:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, semester) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("SEMESTER_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/semester/<string:uid>")
@permission_required(Permission.get("FETCH_SEMESTER"))
def fetch_semester(uid: str) -> Response:
    semester: Union[Semester, None] = Semester.query.filter_by(uid=uid).first()

    if semester:
        return Response(
            json.dumps(semester.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("SEMESTER_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/semester")
@permission_required(Permission.get("CREATE_SEMESTER"))
def add_semester() -> Response:
    response: Dict = {}

    form = AddSemesterForm()

    if form.validate_on_submit():
        semester = Semester()

        semester.name = form.name.data
        semester.number = form.number.data
        semester.department_id = form.department_uid.data

        db.session.add(semester)
        db.session.commit()

        response["message"] = g("SEMESTER_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["title"] = g("SEMESTER_ADDED_LABEL")
        response["category"] = "success"
        response["id"] = getattr(semester, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/semester")
@permission_required(Permission.get("UPDATE_SEMESTER"))
def update_semester() -> Response:
    response: Dict = {}

    form = UpdateSemesterForm()

    if form.validate_on_submit():
        uid = form.uid.data
        semester: Union[Semester, None] = Semester.query.filter_by(uid=uid).first()

        if semester:
            semester.name = form.name.data
            semester.number = form.number.data
            semester.department_id = form.department_uid.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("SEMESTER_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("SEMESTER_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/semester/<string:uid>")
@permission_required(Permission.get("DELETE_SEMESTER"))
def delete_semester(uid: str) -> Response:
    response: Dict = {}

    semester: Union[Semester, None] = Semester.query.filter_by(uid=uid).first()

    if semester:
        db.session.delete(semester)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("SEMESTER_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("SEMESTER_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
