import json
import pathlib
from typing import Dict, List, Tuple, Union

from flask import Response, request
from flask_login import login_required
from sqlalchemy import and_

from app.blueprints.api import bp
from app.extensions import console, db
from app.forms.subject import AddSubjectForm, UpdateSubjectForm
from app.models.file import File, SubjectFile
from app.models.subject import Subject
from app.models.teaching import Teaching
from app.types import ColumnID, ColumnName


@bp.get("/fetch/subjects")
@login_required
def fetch_subjects() -> Response:
    subjects: List[Dict] = [subject.to_dict() for subject in Subject.query.all()]

    return Response(
        json.dumps(subjects),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/subjects")
@login_required
def fetch_subjects_rows() -> Response:
    subjects: List[Subject] = Subject.query.all()

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("UID")),
        (ColumnID("name"), ColumnName("Name")),
        (ColumnID("description"), ColumnName("Description")),
        (ColumnID("credit"), ColumnName("Credit")),
    ]

    rows: List[List] = []

    for subject in subjects:
        dct = subject.to_dict()
        row = [val if (val := dct.get(col_id)) else "N/A" for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/subject/<string:uid>")
@login_required
def fetch_subject_row(uid: str) -> Response:
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
                "message": "Subject with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/subject/<string:uid>")
@login_required
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
                "message": "Subject with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/subject")
@login_required
def add_subject() -> Response:
    response: Dict = {}

    form = AddSubjectForm()

    if form.validate_on_submit():
        subject = Subject()

        subject.name = form.name.data
        subject.description = form.description.data
        subject.department_id = form.department_uid.data
        subject.semester_id = form.semester_uid.data
        if form.credit:
            subject.credit = form.credit.data

        db.session.add(subject)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, link in links.items():
                    match name:
                        case "files":
                            if type(link) == list:
                                files: List[File] = []

                                for l in link:
                                    if File.query.filter_by(file_url=l).first():
                                        continue

                                    path: pathlib.Path = pathlib.Path(l)

                                    file: File = File()

                                    file.file_name = path.name
                                    file.file_url = path
                                    file.file_for = name

                                    db.session.add(file)
                                    files.append(file)

                                db.session.commit()

                                for file in files:
                                    subject_file: SubjectFile = SubjectFile()
                                    subject_file.file_id = file.uid
                                    subject_file.subject_id = subject.uid

                                    db.session.add(subject_file)

                                db.session.commit()

        except Exception as e:
            print(e)

        if form.teachers.data:
            for uid in json.loads(form.teachers.data):
                t = Teaching()
                t.subject_id = subject.uid
                t.teacher_id = uid

                db.session.add(t)

            db.session.commit()

        response["message"] = "Subject added successfully"
        response["category"] = "success"
        response["title"] = "Subject Added"
        response["id"] = subject.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/subject")
@login_required
def update_subject() -> Response:
    response: Dict = {}

    form = UpdateSubjectForm()

    if form.validate_on_submit():
        uid = form.uid.data
        subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()

        if subject:
            subject.name = form.name.data
            subject.description = form.description.data
            subject.department_id = form.department_uid.data
            subject.semester_id = form.semester_uid.data
            if form.credit:
                subject.credit = form.credit.data

            db.session.commit()

            if form.teachers.data:
                nteachers = json.loads(form.teachers.data)
                oteachers = subject.teachings

                for oteacher in oteachers:
                    if oteacher.teacher_id not in nteachers:
                        db.session.delete(oteacher)

                for nteacher in nteachers:
                    if (
                        not db.session.query(Teaching)
                        .filter(
                            and_(
                                Teaching.teacher_id == nteacher,
                                Teaching.subject_id == subject.uid,
                            )
                        )
                        .first()
                    ):
                        t = Teaching()
                        t.teacher_id = nteacher
                        t.subject_id = form.uid.data

                        db.session.add(t)

                db.session.commit()

            else:
                for t in subject.teachings:
                    db.session.delete(t)
                    db.session.commit()

            try:
                links = request.form["links"]
                links = json.loads(links)

                if hasattr(links, "items"):
                    for name, link in links.items():
                        match name:
                            case "files":
                                st: set = set(link)

                                for f in [
                                    f
                                    for f in subject.files
                                    if f.file.file_for == "files"
                                ]:
                                    if f.file.file_url not in st:
                                        db.session.delete(f)
                                        db.session.delete(f.file)

                                db.session.commit()

                                files: List[File] = []
                                for l in st:
                                    if File.query.filter_by(file_url=l).first():
                                        continue

                                    path: pathlib.Path = pathlib.Path(l)
                                    file: File = File()
                                    file.file_name = path.name
                                    file.file_url = path
                                    file.file_for = "resume"

                                    files.append(file)
                                    db.session.add(file)

                                db.session.commit()

                                for f in files:
                                    tf: SubjectFile = SubjectFile()

                                    tf.subject_id = subject.subject_id
                                    tf.file_id = f.uid

                                    db.session.add(tf)

                                if not len(st):
                                    for f in subject.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f.file)
                                            db.session.delete(f)

                                db.session.commit()
            except Exception as err:
                console.print(err)

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Subject updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Subject record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/subject/<string:uid>")
@login_required
def delete_subject(uid: str) -> Response:
    response: Dict = {}

    subject: Union[Subject, None] = Subject.query.filter_by(uid=uid).first()
    if subject:
        db.session.delete(subject)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Subject deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Subject not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
