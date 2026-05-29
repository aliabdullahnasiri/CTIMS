import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.const import DEFAULT_AVATAR, STUDENT
from app.extensions.console import console
from app.extensions.db import db
from app.forms.student import AddStudentForm, UpdateStudentForm
from app.func import render_td
from app.models.permission import Permission
from app.models.role import Role
from app.models.student import Student
from app.models.user import User, permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_student"), ColumnName("Student")),
    (ColumnID("birthday"), ColumnName("Birthday")),
    (ColumnID("age"), ColumnName("Age")),
]


@bp.get("/fetch/students")
@login_required
@permission_required(Permission.get("FETCH_STUDENTS"))
def fetch_students() -> Response:
    students: List[Dict] = [student.to_dict() for student in Student.query.all()]

    return Response(
        json.dumps(students),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/students")
@login_required
@permission_required(Permission.get("FETCH_STUDENTS"))
def fetch_students_rows() -> Response:
    students: List[Student] = Student.query.all()

    rows: List[List] = []

    for student in students:
        row = [render_td(col_id, student) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/student/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_STUDENT"))
def fetch_student_row(uid: str) -> Response:
    student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

    if student:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, student) for col_id, _ in cols],
                    )
                }
            ),
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
@permission_required(Permission.get("FETCH_STUDENT"))
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
@permission_required(Permission.get("CREATE_STUDENT"))
def add_student() -> Response:
    response: Dict = {}

    form = AddStudentForm()

    if form.validate_on_submit():
        user: User = User()

        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.birthday = form.birthday.data
        user.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        if form.password.data:
            user.set_password(form.password.data)

        db.session.add(user)

        if role := Role.get(STUDENT):
            user.primary_role_uid = role.uid

        db.session.commit()

        student = Student()
        student.user_id = getattr(user, "uid")
        student.class_id = form.class_id.data

        db.session.add(student)
        db.session.commit()

        if form.phones.data:
            student.user.update_phones(json.loads(form.phones.data))

        if files := request.form.get("files"):
            try:
                student.user.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        db.session.commit()

        response["message"] = "Student added successfully"
        response["category"] = "success"
        response["title"] = "Student Added"
        response["id"] = getattr(user, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/student")
@login_required
@permission_required(Permission.get("UPDATE_STUDENT") | Permission.get("FETCH_STUDENT"))
def update_student() -> Response:
    response: Dict = {}

    form = UpdateStudentForm()

    if form.validate_on_submit():
        uid = form.uid.data
        student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

        if student:
            student.user.first_name = form.first_name.data
            student.user.middle_name = form.middle_name.data
            student.user.last_name = form.last_name.data
            student.user.user_name = form.user_name.data
            student.user.email = form.email.data
            student.user.birthday = form.birthday.data
            student.class_id = form.class_id.data

            if form.password.data:
                student.user.set_password(form.password.data)

            if form.phones.data:
                student.user.update_phones(json.loads(form.phones.data))

            if files := request.form.get("files"):
                try:
                    student.user.update_files(json.loads(files))
                except json.JSONDecodeError as err:
                    console.print(err)

            db.session.commit()

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
@permission_required(Permission.get("DELETE_STUDENT") | Permission.get("FETCH_STUDENT"))
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
