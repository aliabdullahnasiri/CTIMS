import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.exam import AddExamForm, UpdateExamForm
from app.func import render_td
from app.models.exam import Exam
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("title"), ColumnName(g("TITLE_LABEL"))),
    (ColumnID("description"), ColumnName(g("DESCRIPTION_LABEL"))),
    (ColumnID("total_marks"), ColumnName(g("TOTAL_MARKS_LABEL"))),
    (ColumnID("exam_date"), ColumnName(g("EXAM_DATE_LABEL"))),
    (ColumnID("exam_time"), ColumnName(g("EXAM_TIME_LABEL"))),
]


@bp.get("/fetch/exams")
@permission_required(Permission.get("FETCH_EXAMS"))
def fetch_exams() -> Response:
    exams: List[Dict] = [exam.to_dict() for exam in Exam.query.all()]

    return Response(
        json.dumps(exams),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/exams")
@permission_required(Permission.get("FETCH_EXAMS"))
def fetch_exams_rows() -> Response:
    exams: List[Exam] = Exam.query.all()

    rows: List[List] = []

    for exam in exams:
        row = [render_td(col_id, exam) for col_id, _ in cols]
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


@bp.get("/fetch/row/exam/<string:uid>")
@permission_required(Permission.get("FETCH_EXAM"))
def fetch_exam_row(uid: str) -> Response:
    exam: Union[Exam, None] = Exam.query.filter_by(uid=uid).first()

    if exam:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, exam) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("EXAM_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/exam/<string:uid>")
@permission_required(Permission.get("FETCH_EXAM"))
def fetch_exam(uid: str) -> Response:
    exam: Union[Exam, None] = Exam.query.filter_by(uid=uid).first()

    if exam:
        return Response(
            json.dumps(exam.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("EXAM_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/exam")
@permission_required(Permission.get("CREATE_EXAM"))
def add_exam() -> Response:
    response: Dict = {}

    form = AddExamForm()

    if form.validate_on_submit():
        exam = Exam()

        exam.title = form.title.data
        exam.description = form.description.data
        exam.total_marks = form.total_marks.data
        exam.min_marks = form.min_marks.data
        exam.exam_date = form.exam_date.data
        exam.exam_time = form.exam_time.data
        exam.subject_id = form.subject_id.data
        exam.class_id = form.class_id.data

        db.session.add(exam)
        db.session.commit()

        response["title"] = g("EXAM_ADDED_LABEL")
        response["message"] = g("EXAM_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["id"] = getattr(exam, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/exam")
@permission_required(Permission.get("UPDATE_EXAM") | Permission.get("FETCH_EXAM"))
def update_exam() -> Response:
    response: Dict = {}

    form = UpdateExamForm()

    if form.validate_on_submit():
        uid = form.uid.data
        exam: Union[Exam, None] = Exam.query.filter_by(uid=uid).first()

        if exam:
            exam.title = form.title.data
            exam.description = form.description.data
            exam.total_marks = form.total_marks.data
            exam.min_marks = form.min_marks.data
            exam.exam_date = form.exam_date.data
            exam.exam_time = form.exam_time.data
            exam.subject_id = form.subject_id.data
            exam.class_id = form.class_id.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("EXAM_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("EXAM_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/exam/<string:uid>")
@permission_required(Permission.get("DELETE_EXAM") | Permission.get("FETCH_EXAM"))
def delete_exam(uid: str) -> Response:
    response: Dict = {}

    exam: Union[Exam, None] = Exam.query.filter_by(uid=uid).first()
    if exam:
        db.session.delete(exam)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("EXAM_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("EXAM_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
