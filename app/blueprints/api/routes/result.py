import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.result import AddResultForm, UpdateResultForm
from app.func import render_td
from app.models.permission import Permission
from app.models.result import Result
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("temp_student"), ColumnName(g("STUDENT_LABEL"))),
    (ColumnID("percentage"), ColumnName(g("PERCENTAGE_LABEL"))),
    (ColumnID("temp_result_status"), ColumnName(g("STATUS_LABEL"))),
]


@bp.get("/fetch/results")
@permission_required(Permission.get("FETCH_RESULTS"))
def fetch_results() -> Response:
    results: List[Dict] = [result.to_dict() for result in Result.query.all()]

    return Response(
        json.dumps(results),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/results")
@permission_required(Permission.get("FETCH_RESULTS"))
def fetch_results_rows() -> Response:
    results: List[Result] = Result.query.all()

    rows: List[List] = []

    for result in results:
        row = [render_td(col_id, result) for col_id, _ in cols]
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


@bp.get("/fetch/row/result/<string:uid>")
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
                "message": g("RESULT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/result/<string:uid>")
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
                "message": g("RESULT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/result")
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

        response["message"] = g("RESULT_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["title"] = g("RESULT_ADDED_LABEL")
        response["category"] = "success"
        response["id"] = getattr(result, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/result")
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

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("RESULT_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("RESULT_RECORD_NOT_FOUND_MSG")
            response["category"] = g("ERROR_ERROR")
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/result/<string:uid>")
@permission_required(Permission.get("FETCH_RESULT") | Permission.get("DELETE_RESULT"))
def delete_result(uid: str) -> Response:
    response: Dict = {}

    result: Union[Result, None] = Result.query.filter_by(uid=uid).first()
    if result:
        db.session.delete(result)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("RESULT_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("RESULT_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
