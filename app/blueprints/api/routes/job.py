import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.job import AddJobForm, UpdateJobForm
from app.func import render_td
from app.models.job import Job
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("job_title"), ColumnName(g("JOB_TITLE_LABEL"))),
    (ColumnID("min_salary"), ColumnName(g("MIN_SALARY_LABEL"))),
    (ColumnID("max_salary"), ColumnName(g("MAX_SALARY_LABEL"))),
]


@bp.get("/fetch/jobs")
@permission_required(Permission.get("FETCH_JOBS"))
def fetch_jobs() -> Response:
    jobs: List[Dict] = [job.to_dict() for job in Job.query.all()]

    return Response(
        json.dumps(jobs),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/jobs")
@permission_required(Permission.get("FETCH_JOBS"))
def fetch_jobs_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    jobs: List[Job] = Job.query.all()
    rows: List[List] = []

    for job in jobs:
        row = [render_td(col_id, job) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": [(col_id, g(col_name)) for col_id, col_name in cols],
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/job/<string:uid>")
@permission_required(Permission.get("FETCH_JOB"))
def fetch_job_row(uid: str) -> Response:
    job: Union[Job, None] = Job.query.filter_by(uid=uid).first()

    if job:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, job) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("JOB_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/job/<string:uid>")
@permission_required(Permission.get("FETCH_JOB"))
def fetch_job(uid: str) -> Response:
    job: Union[Job, None] = Job.query.filter_by(uid=uid).first()

    if job:
        return Response(
            json.dumps(job.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("JOB_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/job")
@permission_required(Permission.get("CREATE_JOB"))
def add_job() -> Response:
    response: Dict = {}

    form = AddJobForm()

    if form.validate_on_submit():
        job = Job()

        job.job_title = form.job_title.data
        job.job_description = form.job_description.data
        job.min_salary = form.min_salary.data
        job.max_salary = form.max_salary.data

        db.session.add(job)
        db.session.commit()

        response["title"] = g("JOB_ADDED_LABEL")
        response["message"] = g("JOB_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["id"] = getattr(job, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/job")
@permission_required(Permission.get("UPDATE_JOB"))
def update_job() -> Response:
    response: Dict = {}

    form = UpdateJobForm()

    if form.validate_on_submit():
        uid = form.uid.data
        job: Union[Job, None] = Job.query.filter_by(uid=uid).first()

        if job:
            job.job_title = form.job_title.data
            job.job_description = form.job_description.data
            job.min_salary = form.min_salary.data
            job.max_salary = form.max_salary.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("JOB_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("JOB_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/job/<string:uid>")
@permission_required(Permission.get("DELETE_JOB"))
def delete_job(uid: str) -> Response:
    response: Dict = {}

    job: Union[Job, None] = Job.query.filter_by(uid=uid).first()
    if job:
        db.session.delete(job)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("JOB_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("JOB_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
