import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.time import AddTimeForm, UpdateTimeForm
from app.functions import render_td
from app.models.permission import Permission
from app.models.time import Time
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("title"), ColumnName("Title")),
    (ColumnID("start"), ColumnName("Start Time")),
    (ColumnID("end"), ColumnName("End Time")),
]


@bp.get("/fetch/times")
@login_required
@permission_required(Permission.get("FETCH_TIMES"))
def fetch_times() -> Response:
    times: List[Dict] = [time.to_dict() for time in Time.query.all()]

    return Response(
        json.dumps(times),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/times")
@login_required
@permission_required(Permission.get("FETCH_TIMES"))
def fetch_times_rows() -> Response:
    times: List[Time] = Time.query.all()

    rows: List[List] = []

    for time in times:
        row = [render_td(col_id, time) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/time/<string:uid>")
@login_required
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
                "message": "Time with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/time/<string:uid>")
@login_required
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
                "message": "Time with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/time")
@login_required
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

        response["message"] = "Time added successfully"
        response["category"] = "success"
        response["title"] = "Time Added"
        response["id"] = time.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/time")
@login_required
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

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Time updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Time record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/time/<string:uid>")
@login_required
@permission_required(Permission.get("DELETE_TIME"))
def delete_time(uid: str) -> Response:
    response: Dict = {}

    time: Union[Time, None] = Time.query.filter_by(uid=uid).first()
    if time:
        db.session.delete(time)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Time deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Time not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
