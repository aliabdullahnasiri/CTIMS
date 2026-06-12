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
    (ColumnID("uid"), ColumnName(g("UID"))),
    (ColumnID("temp_hod"), ColumnName(g("Head of department"))),
    (ColumnID("name"), ColumnName(g("name"))),
    (ColumnID("description"), ColumnName(g("Description"))),
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
                "message": g("Department with the given ID was not found :("),
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
                "message": g("Department with the given ID was not found :("),
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

        response["message"] = g("Department added successfully")
        response["category"] = "success"
        response["title"] = g("Department Added")
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

            response["title"] = g("Updated!")
            response["message"] = g("Department updated successfully!")
            response["category"] = "success"
        else:
            response["title"] = g("Not Found")
            response["message"] = g("Department record not found.")
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

        response["title"] = g("Deleted!")
        response["message"] = g("Department deleted successfully")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("Error :(")
        response["message"] = g("Department not found")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
