import json
import re

from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import (
    DateField,
    DecimalField,
    EmailField,
    FileField,
    HiddenField,
    MultipleFileField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from app.extensions import db
from app.functions import validate_uid
from app.models.phone import TeacherPhone
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.time import Time


class AddTeacherForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Optional(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])

    email = EmailField(
        "Email", validators=[DataRequired(), Email("Enter a valid email address")]
    )

    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )

    files = MultipleFileField("Files")
    avatar = FileField("Avatar")

    time_id = StringField("Time UID", validators=[DataRequired(), Length(8, 8)])

    phones = StringField("Phone", validators=[Optional()])
    subjects = StringField("Subject UID", validators=[Optional()])

    submit = SubmitField("Add Teacher")

    # Check if email already exists
    def validate_email(self, email):
        if Teacher.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_time_id(self, time_id) -> None:
        uid = time_id.data

        if not validate_uid(uid):
            raise ValidationError(f"Not a valid Time UID {uid!r}.")

        if not (
            db.session.query(Time)
            .filter(
                Time.uid == uid,
            )
            .first()
        ):

            raise ValidationError("Time with the given ID was not found :(")

    def validate_subjects(self, subjects) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        subjects = json.loads(subjects.data)

        for uid in subjects:
            if not pattern.search(uid):
                raise ValidationError(f"Not a valid Subject UID {uid!r}.")

            if not (
                db.session.query(Subject)
                .filter(
                    Subject.uid == uid,
                )
                .first()
            ):

                raise ValidationError("Teacher with the given ID was not found :(")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(TeacherPhone)
                .filter(
                    TeacherPhone.phone_number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")


class UpdateTeacherForm(AddTeacherForm):
    uid = HiddenField("Teacher ID", validators=[DataRequired()])
    submit = SubmitField("Update Teacher")

    # Check if email already exists
    def validate_email(self, email):
        if (
            db.session.query(Teacher)
            .filter(
                and_(
                    Teacher.uid != self.uid.data,
                    Teacher.email == email.data,
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
                    db.session.query(TeacherPhone)
                    .filter(
                        and_(
                            TeacherPhone.teacher_id != uid,
                            TeacherPhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")
