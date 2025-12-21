import json
import pathlib
from operator import and_
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms.teacher import AddTeacherForm, UpdateTeacherForm
from app.functions import render_td
from app.models.file import File, TeacherFile
from app.models.phone import TeacherPhone
from app.models.teacher import Teacher
from app.models.teaching import Teaching
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_teacher"), ColumnName("Teacher")),
    (ColumnID("birthday"), ColumnName("Birthday")),
    (ColumnID("age"), ColumnName("Age")),
    (ColumnID("salary"), ColumnName("Salary")),
]


@bp.get("/fetch/teachers")
@login_required
def fetch_teachers() -> Response:
    teachers: List[Dict] = [teacher.to_dict() for teacher in Teacher.query.all()]

    return Response(
        json.dumps(teachers),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/teachers")
@login_required
def fetch_teachers_rows() -> Response:
    teachers: List[Teacher] = Teacher.query.all()

    rows: List[List] = []

    for teacher in teachers:
        dct = teacher.to_dict()
        row = [render_td(col_id, teacher) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/teacher/<string:uid>")
@login_required
def fetch_teacher_row(uid: str) -> Response:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(uid=uid).first()

    if teacher:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, teacher) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Teacher with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/teacher/<string:uid>")
@login_required
def fetch_teacher(uid: str) -> Response:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(uid=uid).first()

    if teacher:
        return Response(
            json.dumps(teacher.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Teacher with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/teacher")
@login_required
def add_teacher() -> Response:
    form: AddTeacherForm = AddTeacherForm()

    response: Dict = {}

    if form.validate_on_submit():
        teacher: Teacher = Teacher()

        teacher.first_name = form.first_name.data
        teacher.middle_name = form.middle_name.data
        teacher.last_name = form.last_name.data
        teacher.email = form.email.data
        teacher.birthday = form.birthday.data
        teacher.salary = form.salary.data
        teacher.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        if form.time_id:
            teacher.time_id = form.time_id.data

        db.session.add(teacher)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, link in links.items():
                    match name:
                        case "avatar":
                            teacher.avatar_path = link

                        case "resume":
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
                                    teacher_file: TeacherFile = TeacherFile()
                                    teacher_file.file_id = file.uid
                                    teacher_file.teacher_id = teacher.uid

                                    db.session.add(teacher_file)

                                db.session.commit()

        except Exception as e:
            print(e)

        if form.phones.data:
            for phone in json.loads(form.phones.data):
                teacher_phone = TeacherPhone()
                teacher_phone.teacher_id = teacher.uid
                teacher_phone.phone_number = phone

                db.session.add(teacher_phone)

            db.session.commit()

        if form.subjects.data:
            for uid in json.loads(form.subjects.data):
                t = Teaching()
                t.teacher_id = teacher.uid
                t.subject_id = uid

                db.session.add(t)

            db.session.commit()

        response["message"] = "Teacher added successfully."
        response["title"] = "Added!"
        response["category"] = "success"
        response["id"] = teacher.uid

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)


@bp.post("/update/teacher")
@login_required
def update_teacher() -> Response:
    form: UpdateTeacherForm = UpdateTeacherForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        teacher: Union[Teacher, None] = Teacher.query.filter_by(
            uid=form.uid.data
        ).first()

        if teacher:
            teacher.first_name = form.first_name.data
            teacher.middle_name = form.middle_name.data
            teacher.last_name = form.last_name.data
            teacher.email = form.email.data
            teacher.birthday = form.birthday.data
            teacher.salary = form.salary.data

            if form.time_id:
                teacher.time_id = form.time_id.data

            db.session.commit()

            if form.subjects.data:
                nsubjects = json.loads(form.subjects.data)
                osubjects = teacher.teachings

                for osubject in osubjects:
                    if osubject.subject_id not in nsubjects:
                        db.session.delete(osubject)

                for nsubject in nsubjects:
                    if (
                        not db.session.query(Teaching)
                        .filter(
                            and_(
                                Teaching.subject_id == nsubject,
                                Teaching.teacher_id == teacher.uid,
                            )
                        )
                        .first()
                    ):
                        t = Teaching()
                        t.subject_id = nsubject
                        t.teacher_id = form.uid.data

                        db.session.add(t)

                db.session.commit()

            else:
                for t in teacher.teachings:
                    db.session.delete(t)
                    db.session.commit()

            if form.phones.data:
                nphones = json.loads(form.phones.data)
                ophones = teacher.phones

                for ophone in ophones:
                    if ophone.phone_number not in nphones:
                        db.session.delete(ophone)

                for nphone in nphones:
                    if (
                        not db.session.query(TeacherPhone)
                        .filter(TeacherPhone.phone_number == nphone)
                        .first()
                    ):
                        phone = TeacherPhone()
                        phone.teacher_id = form.uid.data
                        phone.phone_number = nphone

                        db.session.add(phone)

                db.session.commit()
            else:
                for phone in teacher.phones:
                    db.session.delete(phone)

            try:
                links = request.form["links"]
                links = json.loads(links)

                if hasattr(links, "items"):
                    for name, link in links.items():
                        match name:
                            case "avatar":
                                teacher.avatar_path = link

                            case "resume":
                                st: set = set(link)

                                for f in [
                                    f
                                    for f in teacher.files
                                    if f.file.file_for == "resume"
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
                                    tf: TeacherFile = TeacherFile()

                                    tf.teacher_id = teacher.uid
                                    tf.file_id = f.uid

                                    db.session.add(tf)

                                if not len(st):
                                    for f in teacher.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f.file)
                                            db.session.delete(f)

                                db.session.commit()
            except Exception as err:
                console.print(err)

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Teacher updated successfully!",
                    "category": "success",
                }
            )

    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/teacher/<string:uid>")
@login_required
def delete_teacher(uid: str) -> Response:
    response: Dict = {}

    teacher: Union[Teacher, None] = Teacher.query.filter_by(uid=uid).first()
    if teacher:
        db.session.delete(teacher)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Teacher deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Teacher not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
