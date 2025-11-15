import json
import pathlib
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms.student import AddStudentForm, UpdateStudentForm
from app.models.file import File, StudentFile
from app.models.phone import StudentPhone
from app.models.student import Student
from app.types import ColumnID, ColumnName


@bp.get("/fetch/students")
@login_required
def fetch_students() -> Response:
    students: List[Dict] = [student.to_dict() for student in Student.query.all()]

    return Response(
        json.dumps(students),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/students")
@login_required
def fetch_students_rows() -> Response:
    students: List[Student] = Student.query.all()

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("Student UID")),
        (ColumnID("first_name"), ColumnName("First Name")),
        (ColumnID("middle_name"), ColumnName("Middle Name")),
        (ColumnID("last_name"), ColumnName("Last Name")),
        (ColumnID("email"), ColumnName("Email")),
        (ColumnID("birthday"), ColumnName("Birthday")),
    ]

    rows: List[List] = []

    for student in students:
        dct = student.to_dict()
        row = [dct.get(col_id, "N/A") for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/student/<string:uid>")
@login_required
def fetch_student_row(uid: str) -> Response:
    student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

    if student:
        return Response(
            json.dumps(student.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Student with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/student/<string:uid>")
@login_required
def fetch_student(uid: str) -> Response:
    student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

    if student:
        return Response(
            json.dumps(student.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Student with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/student")
@login_required
def add_student() -> Response:
    response: Dict = {}

    form = AddStudentForm()

    if form.validate_on_submit():
        student = Student()

        student.first_name = form.first_name.data
        student.middle_name = form.middle_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.birthday = form.birthday.data
        student.class_id = form.class_id.data
        student.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        db.session.add(student)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, link in links.items():
                    match name:
                        case "avatar":
                            student.avatar_path = link

        except Exception as e:
            print(e)

        if form.phones.data:
            for phone in json.loads(form.phones.data):
                student_phone = StudentPhone()
                student_phone.student_id = student.uid
                student_phone.phone_number = phone

                db.session.add(student_phone)

            db.session.commit()

        response["message"] = "Student added successfully"
        response["category"] = "success"
        response["title"] = "Student Added"
        response["id"] = student.uid

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/student")
@login_required
def update_student() -> Response:
    response: Dict = {}

    form = UpdateStudentForm()

    if form.validate_on_submit():
        uid = form.uid.data
        student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

        if student:
            student.first_name = form.first_name.data
            student.middle_name = form.middle_name.data
            student.last_name = form.last_name.data
            student.email = form.email.data
            student.birthday = form.birthday.data
            student.class_id = form.class_id.data

            db.session.commit()

            if form.phones.data:
                nphones = json.loads(form.phones.data)
                ophones = student.phones

                for ophone in ophones:
                    if ophone.phone_number not in nphones:
                        db.session.delete(ophone)

                for nphone in nphones:
                    if (
                        not db.session.query(StudentPhone)
                        .filter(StudentPhone.phone_number == nphone)
                        .first()
                    ):
                        phone = StudentPhone()
                        phone.student_id = form.uid.data
                        phone.phone_number = nphone

                        db.session.add(phone)
            else:
                for phone in student.phones:
                    db.session.delete(phone)

            try:
                links = request.form["links"]
                links = json.loads(links)

                print(links)

                if hasattr(links, "items"):
                    for name, link in links.items():
                        match name:
                            case "avatar":
                                student.avatar_path = link

                            case "files":
                                st: set = set(link)

                                for f in [f for f in student.files]:
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

                                    files.append(file)
                                    db.session.add(file)

                                db.session.commit()

                                for f in files:
                                    tf: StudentFile = StudentFile()

                                    tf.student_id = student.uid
                                    tf.file_id = f.uid

                                    db.session.add(tf)

                                if not len(st):
                                    for f in student.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f.file)
                                            db.session.delete(f)

                                db.session.commit()

            except Exception as err:
                console.print(err)

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Student updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Student record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/student/<string:uid>")
@login_required
def delete_student(uid: str) -> Response:
    response: Dict = {}

    student: Union[Student, None] = Student.query.filter_by(uid=uid).first()
    if student:
        db.session.delete(student)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Student deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Student not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
