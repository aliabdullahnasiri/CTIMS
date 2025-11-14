import json
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional

from app.extensions import db
from app.models.department import Department
from app.models.semester import Semester
from app.models.teacher import Teacher


class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Subject Description", validators=[Optional(), Length(max=2000)]
    )
    credit = IntegerField("Credit", validators=[Optional()])

    department_uid = StringField("Department UID", validators=[DataRequired()])
    semester_uid = StringField("Semester UID", validators=[DataRequired()])

    teachers = StringField("Teacher UID", validators=[Optional()])

    files = MultipleFileField(
        "Files",
        validators=[FileAllowed(["pdf"], "PDF only!")],
    )

    submit = SubmitField("Add Semester")

    def validate_department_uid(self, department_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(department_uid.data):
            raise ValidationError("Not a valid Department UID.")
        elif not Department.query.filter_by(uid=department_uid.data).first():
            raise ValidationError("Department with the given ID was not found :(")

    def validate_semester_uid(self, semester_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(semester_uid.data):
            raise ValidationError("Not a valid Semester UID.")
        elif not Semester.query.filter_by(uid=semester_uid.data).first():
            raise ValidationError("Semester with the given ID was not found :(")

    def validate_teachers(self, teachers) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        teachers = json.loads(teachers.data)

        for uid in teachers:
            if not pattern.search(uid):
                raise ValidationError(f"Not a valid Teacher UID {uid!r}.")

            if not (
                db.session.query(Teacher)
                .filter(
                    Teacher.uid == uid,
                )
                .first()
            ):

                raise ValidationError("Teacher with the given ID was not found :(")


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField("Subject UID", validators=[DataRequired()])

    submit = SubmitField("Update Subject")
