import json
from re import sub
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.const import DEFAULT_AVATAR, STUDENT
from app.extensions.console import console
from app.extensions.db import db
from app.forms.student import AddStudentForm, UpdateStudentForm
from app.func import render_td
from app.models.permission import Permission
from app.models.role import Role
from app.models.student import IdentityCardType, Student
from app.models.subject import StudentSubject
from app.models.user import User, permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("temp_student"), ColumnName(g("STUDENT_LABEL"))),
    (ColumnID("birthday"), ColumnName(g("BIRTHDAY_LABEL"))),
    (ColumnID("age"), ColumnName(g("AGE_LABEL"))),
]


@bp.get("/fetch/students")
@permission_required(Permission.get("FETCH_STUDENTS"))
def fetch_students() -> Response:
    students: List[Dict] = [student.to_dict() for student in Student.query.all()]

    return Response(
        json.dumps(students),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/students")
@permission_required(Permission.get("FETCH_STUDENTS"))
def fetch_students_rows() -> Response:
    students: List[Student] = Student.query.all()

    rows: List[List] = []

    for student in students:
        row = [render_td(col_id, student) for col_id, _ in cols]
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


@bp.get("/fetch/row/student/<string:uid>")
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
                "message": g("STUDENT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/student/<string:uid>")
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
                "message": g("STUDENT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/student")
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
            user.update_roles(primary_role=role)

        db.session.commit()

        student = Student()
        student.user_id = getattr(user, "uid")

        student.father_name = form.father_name.data
        student.grandfather_name = form.grandfather_name.data
        student.kankor_id = form.kankor_id.data

        student.daily_section_uid = form.daily_section_uid.data

        student.electronic_tazkira_number = form.electronic_tazkira_number.data

        student.tazkira_folder = form.tazkira_folder.data
        student.tazkira_page_number = form.tazkira_page_number.data
        student.tazkira_registration_number = form.tazkira_registration_number.data
        student.tazkira_sakok_number = form.tazkira_sakok_number.data

        student.permanent_province_uid = form.permanent_province.data
        student.permanent_district_uid = form.permanent_district.data
        student.permanent_village = form.permanent_village.data

        student.current_province_uid = form.current_province.data
        student.current_district_uid = form.current_district.data
        student.current_village = form.current_village.data

        if form.identity_card_type.data == IdentityCardType.ELECTRONIC:
            student.tazkira_folder = None
            student.tazkira_page_number = None
            student.tazkira_registration_number = None
            student.tazkira_sakok_number = None

        elif form.identity_card_type.data == IdentityCardType.PAPER:
            student.electronic_tazkira_number = None

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

        response["message"] = g("STUDENT_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["title"] = g("STUDENT_ADDED_LABEL")
        response["category"] = "success"
        response["id"] = getattr(student, "uid")

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/student")
@permission_required(Permission.get("UPDATE_STUDENT") | Permission.get("FETCH_STUDENT"))
def update_student() -> Response:
    response: Dict = {}

    form = UpdateStudentForm()

    if form.validate_on_submit():
        uid = form.uid.data
        student: Union[Student, None] = Student.query.filter_by(uid=uid).first()

        print(student.updated_at)
        if student:
            student.user.first_name = form.first_name.data
            student.user.middle_name = form.middle_name.data
            student.user.last_name = form.last_name.data
            student.user.user_name = form.user_name.data
            student.user.email = form.email.data
            student.user.birthday = form.birthday.data

            student.class_id = form.class_id.data
            student.daily_section_uid = form.daily_section_uid.data

            student.father_name = form.father_name.data
            student.grandfather_name = form.grandfather_name.data
            student.kankor_id = form.kankor_id.data

            student.electronic_tazkira_number = form.electronic_tazkira_number.data

            student.tazkira_folder = form.tazkira_folder.data
            student.tazkira_page_number = form.tazkira_page_number.data
            student.tazkira_registration_number = form.tazkira_registration_number.data
            student.tazkira_sakok_number = form.tazkira_sakok_number.data

            student.permanent_province_uid = form.permanent_province.data
            student.permanent_district_uid = form.permanent_district.data
            student.permanent_village = form.permanent_village.data

            student.current_province_uid = form.current_province.data
            student.current_district_uid = form.current_district.data
            student.current_village = form.current_village.data
            student.high_school_name = form.high_school_name.data
            student.high_school_registration_no = form.high_school_registration_no.data
            student.high_school_graduation_year = form.high_school_graduation_year.data
            student.high_school_province_uid = form.high_school_province.data
            student.father_job = form.father_job.data
            student.father_job_address = form.father_job_address.data

            if form.identity_card_type.data == IdentityCardType.ELECTRONIC:
                student.tazkira_folder = None
                student.tazkira_page_number = None
                student.tazkira_registration_number = None
                student.tazkira_sakok_number = None

            elif form.identity_card_type.data == IdentityCardType.PAPER:
                student.electronic_tazkira_number = None

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

            for (grade_uid, subject_uid), score in dict(
                map(
                    lambda item: (tuple(item[0].split("_")[1:]), int(item[1])),
                    filter(
                        lambda item: item[0].startswith("GRADE_"),
                        list(request.form.items()),
                    ),
                )
            ).items():
                student_subject = StudentSubject.query.filter_by(
                    student_uid=student.uid,
                    subject_uid=subject_uid,
                    grade_uid=grade_uid,
                ).first()

                if student_subject:
                    student_subject.score = score
                else:
                    s = StudentSubject()
                    s.subject_uid = subject_uid
                    s.student_uid = student.uid
                    s.grade_uid = grade_uid
                    s.score = score

                    db.session.add(s)

                student.update()

                db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("STUDENT_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("STUDENT_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = dict(form.errors) | form.errors_dct

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/student/<string:uid>")
@permission_required(Permission.get("DELETE_STUDENT") | Permission.get("FETCH_STUDENT"))
def delete_student(uid: str) -> Response:
    response: Dict = {}

    student: Union[Student, None] = Student.query.filter_by(uid=uid).first()
    if student:
        db.session.delete(student)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g("STUDENT_DELETED_SUCCESSFULLY_SUCCESS_MSG")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("STUDENT_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
