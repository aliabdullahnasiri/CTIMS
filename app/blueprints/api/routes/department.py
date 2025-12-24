import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.department import AddDepartmentForm, UpdateDepartmentForm
from app.functions import render_td
from app.models.department import Department
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("name"), ColumnName("name")),
    (ColumnID("description"), ColumnName("Description")),
]


@bp.get("/fetch/departments")
@login_required
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
@login_required
def fetch_departments_rows() -> Response:
    departments: List[Department] = Department.query.all()

    rows: List[List] = []

    for department in departments:
        dct = department.to_dict()
        row = [render_td(col_id, department) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/department/<string:uid>")
@login_required
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
                "message": "Department with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/department/<string:uid>")
@login_required
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
                "message": "Department with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/department")
@login_required
def add_department() -> Response:
    response: Dict = {}

    form = AddDepartmentForm()

    if form.validate_on_submit():
        department = Department()

        department.name = form.name.data
        department.description = form.description.data
        department.head_of_department = form.head_of_department.data

        db.session.add(department)
        db.session.commit()

        response["message"] = "Department added successfully"
        response["category"] = "success"
        response["title"] = "Department Added"
        response["id"] = department.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/department")
@login_required
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

            db.session.commit()

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Department updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Department record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/department/<string:uid>")
@login_required
def delete_department(uid: str) -> Response:
    response: Dict = {}

    department: Union[Department, None] = Department.query.filter_by(uid=uid).first()
    if department:
        db.session.delete(department)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Department deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Department not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
