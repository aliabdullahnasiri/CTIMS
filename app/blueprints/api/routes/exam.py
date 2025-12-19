import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.exam import AddExamForm, UpdateExamForm
from app.functions import render_td
from app.models.exam import Exam
from app.types import ColumnID, ColumnName


@bp.get("/fetch/exams")
@login_required
def fetch_exams() -> Response:
    exams: List[Dict] = [exam.to_dict() for exam in Exam.query.all()]

    return Response(
        json.dumps(exams),
        status=200,
        headers={"Content-Type": "application/json"},
    )


cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("title"), ColumnName("Title")),
    (ColumnID("description"), ColumnName("Description")),
    (ColumnID("total_marks"), ColumnName("Total Marks")),
    (ColumnID("exam_date"), ColumnName("Exam Date")),
    (ColumnID("exam_time"), ColumnName("Exam Time")),
]


@bp.get("/fetch/rows/exams")
@login_required
def fetch_exams_rows() -> Response:
    exams: List[Exam] = Exam.query.all()

    rows: List[List] = []

    for exam in exams:
        row = [render_td(col_id, exam) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/exam/<string:uid>")
@login_required
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
                "message": "Exam with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/exam/<string:uid>")
@login_required
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
                "message": "Exam with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/exam")
@login_required
def add_exam() -> Response:
    response: Dict = {}

    form = AddExamForm()

    if form.validate_on_submit():
        exam = Exam()

        exam.title = form.title.data
        exam.description = form.description.data
        exam.total_marks = form.total_marks.data
        exam.exam_date = form.exam_date.data
        exam.exam_time = form.exam_time.data
        exam.subject_id = form.subject_id.data
        exam.class_id = form.class_id.data

        db.session.add(exam)
        db.session.commit()

        response["message"] = "Exam added successfully"
        response["category"] = "success"
        response["title"] = "Exam Added"
        response["id"] = exam.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/exam")
@login_required
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
            exam.exam_date = form.exam_date.data
            exam.exam_time = form.exam_time.data
            exam.subject_id = form.subject_id.data
            exam.class_id = form.class_id.data

            db.session.commit()

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Exam updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Exam record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/exam/<string:uid>")
@login_required
def delete_exam(uid: str) -> Response:
    response: Dict = {}

    exam: Union[Exam, None] = Exam.query.filter_by(uid=uid).first()
    if exam:
        db.session.delete(exam)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Exam deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Exam not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
