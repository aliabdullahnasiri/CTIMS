import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.department import AddDepartmentForm, UpdateDepartmentForm
from app.func import render_td
from app.models.department import Department
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("temp_hod"), ColumnName(g("HEAD_OF_DEPARTMENT_MSG"))),
    (ColumnID("name"), ColumnName(g("NAME_LABEL"))),
    (ColumnID("description"), ColumnName(g("DESCRIPTION_LABEL"))),
]


@bp.get("/fetch/departments")
@permission_required(Permission.get("FETCH_DEPARTMENTS"))
def fetch_departments() -> Response:
    departments: List[Dict] = [
        department.to_dict() for department in Department.query.all()
    ]

    return Response(
        json.dumps(departments),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/departments")
@permission_required(Permission.get("FETCH_DEPARTMENTS"))
def fetch_departments_rows() -> Response:
    departments: List[Department] = Department.query.all()

    rows: List[List] = []

    for department in departments:
        row = [render_td(col_id, department) for col_id, _ in cols]
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


@bp.get("/fetch/row/department/<string:uid>")
@permission_required(Permission.get("FETCH_DEPARTMENT"))
def fetch_department_row(uid: str) -> Response:
    department: Union[Department, None] = Department.query.filter_by(uid=uid).first()

    if department:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, department) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("DEPARTMENT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/department/<string:uid>")
@permission_required(Permission.get("FETCH_DEPARTMENT"))
def fetch_department(uid: str) -> Response:
    department: Union[Department, None] = Department.query.filter_by(uid=uid).first()

    if department:
        return Response(
            json.dumps(department.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("DEPARTMENT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/department")
@permission_required(Permission.get("CREATE_DEPARTMENT"))
def add_department() -> Response:
    response: Dict = {}

    form = AddDepartmentForm()

    if form.validate_on_submit():
        department = Department()

        department.name = form.name.data
        department.description = form.description.data

        department.head_of_department = (
            uid if (uid := form.head_of_department.data) else None
        )
        department.parent_department_uid = (
            uid if (uid := form.parent_department_uid.data) else None
        )

        db.session.add(department)
        db.session.commit()

        response["message"] = g("DEPARTMENT_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["title"] = g("DEPARTMENT_ADDED_LABEL")
        response["id"] = getattr(department, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/department")
@permission_required(Permission.get("UPDATE_DEPARTMENT"))
def update_department() -> Response:
    response: Dict = {}

    form = UpdateDepartmentForm()

    if form.validate_on_submit():
        uid = form.uid.data
        department: Union[Department, None] = Department.query.filter_by(
            uid=uid
        ).first()

        if department:
            department.name = form.name.data
            department.description = form.description.data
            department.head_of_department = form.head_of_department.data
            department.parent_department_uid = form.parent_department_uid.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("DEPARTMENT_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("DEPARTMENT_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/department/<string:uid>")
@permission_required(Permission.get("DELETE_DEPARTMENT"))
def delete_department(uid: str) -> Response:
    response: Dict = {}

    department = Department.query.filter_by(uid=uid).scalar()
    if department:
        if department.uid == department.parent_department_uid:
            department.parent_department_uid = None
            db.session.commit()

        db.session.delete(department)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("DEPARTMENT_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("DEPARTMENT_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
