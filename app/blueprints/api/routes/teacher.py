import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms.teacher import AddTeacherForm, UpdateTeacherForm
from app.functions import render_td
from app.models.permission import Permission
from app.models.role import Role
from app.models.teacher import Teacher
from app.models.user import User, permission_required
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
@permission_required(Permission.get("FETCH_TEACHERS"))
def fetch_teachers() -> Response:
    teachers: List[Dict] = [teacher.to_dict() for teacher in Teacher.query.all()]

    return Response(
        json.dumps(teachers),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/teachers")
@login_required
@permission_required(Permission.get("FETCH_TEACHERS"))
def fetch_teachers_rows() -> Response:
    teachers: List[Teacher] = Teacher.query.all()

    rows: List[List] = []

    for teacher in teachers:
        row = [render_td(col_id, teacher) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/teacher/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_TEACHER"))
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
@permission_required(Permission.get("FETCH_TEACHER"))
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
@permission_required(Permission.get("CREATE_TEACHER"))
def add_teacher() -> Response:
    form: AddTeacherForm = AddTeacherForm()

    response: Dict = {}

    if form.validate_on_submit():
        user: User = User()

        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.birthday = form.birthday.data
        user.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        if role := Role.query.filter_by(name=Role.get("TEACHER")).first():
            user.role_uid = role.uid

        if form.password.data:
            user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        teacher: Teacher = Teacher()

        teacher.user_uid = user.uid
        teacher.salary = form.salary.data
        teacher.time_id = form.time_id.data

        db.session.add(teacher)
        db.session.commit()

        if form.subjects.data:
            teacher.update_subjects(json.loads(form.subjects.data))

        if form.phones.data:
            teacher.user.update_phones(json.loads(form.phones.data))

        if files := request.form.get("files"):
            try:
                teacher.user.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        response["message"] = "Teacher added successfully."
        response["title"] = "Added!"
        response["category"] = "success"
        response["id"] = teacher.uid

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)


@bp.post("/update/teacher")
@login_required
@permission_required(Permission.get("UPDATE_TEACHER") | Permission.get("FETCH_TEACHER"))
def update_teacher() -> Response:
    form: UpdateTeacherForm = UpdateTeacherForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        teacher: Union[Teacher, None] = Teacher.query.filter_by(
            uid=form.uid.data
        ).first()

        if teacher:
            teacher.user.first_name = form.first_name.data
            teacher.user.middle_name = form.middle_name.data
            teacher.user.last_name = form.last_name.data
            teacher.user.email = form.email.data
            teacher.user.birthday = form.birthday.data

            teacher.salary = form.salary.data
            teacher.time_id = form.time_id.data

            db.session.commit()

            if form.subjects.data:
                teacher.update_subjects(json.loads(form.subjects.data))

            if form.phones.data:
                teacher.user.update_phones(json.loads(form.phones.data))

            if files := request.form.get("files"):
                try:
                    teacher.user.update_files(json.loads(files))
                except json.JSONDecodeError as err:
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
@permission_required(Permission.get("DELETE_TEACHER") | Permission.get("FETCH_TEACHER"))
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
