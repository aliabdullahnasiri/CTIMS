import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions.db import db
from app.forms.result import AddResultForm, UpdateResultForm
from app.func import render_td
from app.models.permission import Permission
from app.models.result import Result
from app.models.user import permission_required
from app.cls import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_student"), ColumnName("Student")),
    (ColumnID("percentage"), ColumnName("Percentage")),
    (ColumnID("temp_result_status"), ColumnName("Status")),
]


@bp.get("/fetch/results")
@login_required
@permission_required(Permission.get("FETCH_RESULTS"))
def fetch_results() -> Response:
    results: List[Dict] = [result.to_dict() for result in Result.query.all()]

    return Response(
        json.dumps(results),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/results")
@login_required
@permission_required(Permission.get("FETCH_RESULTS"))
def fetch_results_rows() -> Response:
    results: List[Result] = Result.query.all()

    rows: List[List] = []

    for result in results:
        row = [render_td(col_id, result) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/result/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_RESULT"))
def fetch_result_row(uid: str) -> Response:
    result: Union[Result, None] = Result.query.filter_by(uid=uid).first()

    if result:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, result) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Result with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/result/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_RESULT"))
def fetch_result(uid: str) -> Response:
    result: Union[Result, None] = Result.query.filter_by(uid=uid).first()

    if result:
        return Response(
            json.dumps(result.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Result with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/result")
@login_required
@permission_required(Permission.get("FETCH_RESULT") | Permission.get("CREATE_RESULT"))
def add_result() -> Response:
    response: Dict = {}

    form = AddResultForm()

    if form.validate_on_submit():
        result = Result()

        result.obtained_marks = form.obtained_marks.data
        result.exam_id = form.exam_id.data
        result.student_id = form.student_id.data

        db.session.add(result)
        db.session.commit()

        response["message"] = "Result added successfully"
        response["category"] = "success"
        response["title"] = "Result Added"
        response["id"] = result.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/result")
@login_required
@permission_required(Permission.get("FETCH_RESULT") | Permission.get("UPDATE_RESULT"))
def update_result() -> Response:
    response: Dict = {}

    form = UpdateResultForm()

    if form.validate_on_submit():
        uid = form.uid.data
        result: Union[Result, None] = Result.query.filter_by(uid=uid).first()

        if result:
            result.obtained_marks = form.obtained_marks.data
            result.exam_id = form.exam_id.data
            result.student_id = form.student_id.data

            db.session.commit()

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Result updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Result record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/result/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_RESULT") | Permission.get("DELETE_RESULT"))
def delete_result(uid: str) -> Response:
    response: Dict = {}

    result: Union[Result, None] = Result.query.filter_by(uid=uid).first()
    if result:
        db.session.delete(result)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Result deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Result not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
