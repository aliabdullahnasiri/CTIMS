import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.time import AddTimeForm, UpdateTimeForm
from app.func import render_td
from app.models.permission import Permission
from app.models.time import Time
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("title"), ColumnName(g("TITLE_LABEL"))),
    (ColumnID("start"), ColumnName(g("START_TIME_LABEL"))),
    (ColumnID("end"), ColumnName(g("END_TIME_LABEL"))),
]


@bp.get("/fetch/times")
@permission_required(Permission.get("FETCH_TIMES"))
def fetch_times() -> Response:
    times: List[Dict] = [time.to_dict() for time in Time.query.all()]

    return Response(
        json.dumps(times),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/times")
@permission_required(Permission.get("FETCH_TIMES"))
def fetch_times_rows() -> Response:
    times: List[Time] = Time.query.all()

    rows: List[List] = []

    for time in times:
        row = [render_td(col_id, time) for col_id, _ in cols]
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


@bp.get("/fetch/row/time/<string:uid>")
@permission_required(Permission.get("FETCH_TIME"))
def fetch_time_row(uid: str) -> Response:
    time: Union[Time, None] = Time.query.filter_by(uid=uid).first()

    if time:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, time) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("TIME_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/time/<string:uid>")
@permission_required(Permission.get("FETCH_TIME"))
def fetch_time(uid: str) -> Response:
    time: Union[Time, None] = Time.query.filter_by(uid=uid).first()

    if time:
        return Response(
            json.dumps(time.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("TIME_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/time")
@permission_required(Permission.get("CREATE_TIME"))
def add_time() -> Response:
    response: Dict = {}

    form = AddTimeForm()

    if form.validate_on_submit():
        time = Time()

        time.title = form.title.data
        time.description = form.description.data
        time.start = form.start.data
        time.end = form.end.data

        db.session.add(time)
        db.session.commit()

        response["message"] = g("TIME_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["title"] = g("TIME_ADDED_LABEL")
        response["category"] = "success"
        response["id"] = getattr(time, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/time")
@permission_required(Permission.get("UPDATE_TIME"))
def update_time() -> Response:
    response: Dict = {}

    form = UpdateTimeForm()

    if form.validate_on_submit():
        uid = form.uid.data
        time: Union[Time, None] = Time.query.filter_by(uid=uid).first()

        if time:
            time.title = form.title.data
            time.description = form.description.data
            time.start = form.start.data
            time.end = form.end.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("TIME_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("TIME_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/time/<string:uid>")
@permission_required(Permission.get("DELETE_TIME"))
def delete_time(uid: str) -> Response:
    response: Dict = {}

    time: Union[Time, None] = Time.query.filter_by(uid=uid).first()
    if time:
        db.session.delete(time)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("TIME_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("TIME_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
