import json
from typing import Dict, List, Tuple, Union

from flask import Response, request
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.console import console
from app.extensions.db import db
from app.forms.subject import AddSubjectForm, UpdateSubjectForm
from app.func import render_td
from app.models.permission import Permission
from app.models.subject import Subject
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID"))),
    (ColumnID("name"), ColumnName(g("Name"))),
    (ColumnID("description"), ColumnName(g("Description"))),
    (ColumnID("credit"), ColumnName(g("Credit"))),
]


@bp.get("/fetch/subjects")
@permission_required(Permission.get("FETCH_SUBJECTS"))
def fetch_subjects() -> Response:
    subjects: List[Dict] = [subject.to_dict() for subject in Subject.query.all()]

    return Response(
        json.dumps(subjects),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/subjects")
@permission_required(Permission.get("FETCH_SUBJECTS"))
def fetch_subjects_rows() -> Response:
    subjects: List[Subject] = Subject.query.all()

    rows: List[List] = []

    for subject in subjects:
        row = [render_td(col_id, subject) for col_id, _ in cols]
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


@bp.get("/fetch/row/subject/<string:uid>")
@permission_required(Permission.get("FETCH_SUBJECT"))
def fetch_subject_row(uid: str) -> Response:
    subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()

    if subject:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, subject) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("Subject with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/subject/<string:uid>")
@permission_required(Permission.get("FETCH_SUBJECT"))
def fetch_subject(uid: str) -> Response:
    subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()

    if subject:
        return Response(
            json.dumps(subject.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("Subject with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/subject")
@permission_required(Permission.get("CREATE_SUBJECT"))
def add_subject() -> Response:
    response: Dict = {}

    form = AddSubjectForm()

    if form.validate_on_submit():
        subject = Subject()

        subject.name = form.name.data
        subject.description = form.description.data
        subject.semester_id = form.semester_uid.data
        if form.credit:
            subject.credit = form.credit.data

        db.session.add(subject)

        if files := request.form.get("files"):
            try:
                subject.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        db.session.commit()

        response["title"] = g("Subject Added")
        response["message"] = g("Subject added successfully")
        response["category"] = "success"
        response["id"] = getattr(subject, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/subject")
@permission_required(Permission.get("FETCH_SUBJECT") | Permission.get("UPDATE_SUBJECT"))
def update_subject() -> Response:
    response: Dict = {}

    form = UpdateSubjectForm()

    if form.validate_on_submit():
        uid = form.uid.data
        subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()

        if subject:
            subject.name = form.name.data
            subject.description = form.description.data
            subject.semester_id = form.semester_uid.data
            if form.credit:
                subject.credit = form.credit.data

            if files := request.form.get("files"):
                try:
                    subject.update_files(json.loads(files))
                except json.JSONDecodeError as err:
                    console.print(err)

            db.session.commit()

            response["title"] = g("Updated!")
            response["message"] = g("Subject updated successfully!")
            response["category"] = "success"
        else:
            response["title"] = g("Not Found")
            response["message"] = g("Subject record not found.")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/subject/<string:uid>")
@permission_required(Permission.get("FETCH_SUBJECT") | Permission.get("DELETE_SUBJECT"))
def delete_subject(uid: str) -> Response:
    response: Dict = {}

    subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()

    if subject:
        db.session.delete(subject)
        db.session.commit()

        response["title"] = g("Deleted!")
        response["message"] = g("Subject deleted successfully")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("Error :(")
        response["message"] = g("Subject not found")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
