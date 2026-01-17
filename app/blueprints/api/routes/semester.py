import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.semester import AddSemesterForm, UpdateSemesterForm
from app.functions import render_td
from app.models.semester import Semester
from app.models.user import PermissionEnum, permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("name"), ColumnName("Name")),
    (ColumnID("number"), ColumnName("Number")),
]


@bp.get("/fetch/semesters")
@login_required
@permission_required(PermissionEnum.FETCH_SEMESTERS.value)
def fetch_semesters() -> Response:
    semesters: List[Dict] = [semester.to_dict() for semester in Semester.query.all()]

    return Response(
        json.dumps(semesters),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/semesters")
@login_required
@permission_required(PermissionEnum.FETCH_SEMESTERS.value)
def fetch_semesters_rows() -> Response:
    semesters: List[Semester] = Semester.query.all()

    rows: List[List] = []

    for semester in semesters:
        row = [render_td(col_id, semester) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/semester/<string:uid>")
@login_required
@permission_required(PermissionEnum.FETCH_SEMESTER.value)
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
                "message": "Semester with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/semester/<string:uid>")
@login_required
@permission_required(PermissionEnum.FETCH_SEMESTER.value)
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
                "message": "Semester with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/semester")
@login_required
@permission_required(PermissionEnum.CREATE_SEMESTER.value)
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

        response["message"] = "Semester added successfully"
        response["category"] = "success"
        response["title"] = "Semester Added"
        response["id"] = semester.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/semester")
@login_required
@permission_required(PermissionEnum.UPDATE_SEMESTER.value)
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

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Semester updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Semester record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/semester/<string:uid>")
@login_required
@permission_required(PermissionEnum.DELETE_SEMESTER.value)
def delete_semester(uid: str) -> Response:
    response: Dict = {}

    semester: Union[Semester, None] = Semester.query.filter_by(uid=uid).first()
    if semester:
        db.session.delete(semester)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Semester deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Semester not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
