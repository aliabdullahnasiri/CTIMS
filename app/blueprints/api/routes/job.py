import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.job import AddJobForm, UpdateJobForm
from app.models.job import Job
from app.types import ColumnID, ColumnName


@bp.get("/fetch/jobs")
@login_required
def fetch_jobs() -> Response:
    jobs: List[Dict] = [job.to_dict() for job in Job.query.all()]

    return Response(
        json.dumps(jobs),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/jobs")
@login_required
def fetch_jobs_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("Job UID")),
        (ColumnID("job_title"), ColumnName("Job Title")),
        (ColumnID("min_salary"), ColumnName("Min Salary")),
        (ColumnID("max_salary"), ColumnName("Max Salary")),
    ]

    jobs: List[Job] = Job.query.all()
    rows: List[List] = []

    for job in jobs:
        row: List = []

        for col_id, _ in cols:
            val = getattr(job, col_id)

            match col_id:
                case "min_salary":
                    row.append(job.display_min_salary)

                case "max_salary":
                    row.append(job.display_max_salary)

                case _:
                    row.append(val)

        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/job/<string:uid>")
@login_required
def fetch_job_row(uid: str) -> Response:
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
                "message": "Job with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/job/<string:uid>")
@login_required
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
                "message": "Job with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/job")
@login_required
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

        response["message"] = "Job added successfully"
        response["category"] = "success"
        response["title"] = "Job Added"
        response["id"] = job.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/job")
@login_required
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

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Job updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Job record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/job/<string:uid>")
@login_required
def delete_job(uid: str) -> Response:
    response: Dict = {}

    job: Union[Job, None] = Job.query.filter_by(uid=uid).first()
    if job:
        db.session.delete(job)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Job deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Job not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
