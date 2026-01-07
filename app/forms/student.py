import json
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from sqlalchemy import and_
from wtforms import (
    DateField,
    FileField,
    HiddenField,
    MultipleFileField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

from app.models.class_ import Class
from app.models.phone import StudentPhone

from ..extensions import db
from ..models.job import Job
from ..models.student import Student


class AddStudentForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField("Upload new profile picture")
    files = MultipleFileField("Files")
    phones = StringField("Phone", validators=[Optional()])
    class_id = StringField("Class UID", validators=[DataRequired(), Length(8, 8)])
    submit = SubmitField("Add")

    def validate_class_id(self, class_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(class_id.data):
            raise ValidationError("Not a valid Class UID.")
        elif not Class.query.filter_by(uid=class_id.data).first():
            raise ValidationError("Class with the given ID was not found :(")

    # Check if email already exists
    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(StudentPhone)
                .filter(
                    StudentPhone.phone_number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")

    def validate_job_id(self, job_id) -> None:
        pattern: re.Pattern = re.compile(r"^\d{0,}$")

        if not pattern.search(job_id.data):
            raise ValidationError("Not a valid decimal value.")
        elif not Job.query.filter_by(job_id=int(job_id.data)).first():
            raise ValidationError("Job with the given ID was not found :(")


class UpdateStudentForm(AddStudentForm):
    uid = HiddenField("Student UID", validators=[DataRequired()])
    files = MultipleFileField(
        "Files",
        validators=[],
    )
    submit = SubmitField("Update Student")

    # Check if email already exists
    def validate_email(self, email):
        if (
            db.session.query(Student)
            .filter(
                and_(
                    Student.uid != self.uid.data,
                    Student.email == email.data,
                )
            )
            .first()
        ):
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        if hasattr(self, "uid"):
            uid = self.uid.data

            for num in nums:
                if (
                    db.session.query(StudentPhone)
                    .filter(
                        and_(
                            StudentPhone.student_id != uid,
                            StudentPhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")
