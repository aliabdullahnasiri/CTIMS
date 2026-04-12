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

from app.models.semester import Semester


class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Subject Description", validators=[Optional(), Length(max=2000)]
    )
    credit = IntegerField("Credit", validators=[Optional()])

    semester_uid = StringField("Semester UID", validators=[DataRequired()])

    files = MultipleFileField("Files")

    submit = SubmitField("Add Subject")

    def validate_semester_uid(self, semester_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(semester_uid.data):
            raise ValidationError("Not a valid Semester UID.")
        elif not Semester.query.filter_by(uid=semester_uid.data).first():
            raise ValidationError("Semester with the given ID was not found :(")


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField("Subject UID", validators=[DataRequired()])

    submit = SubmitField("Update Subject")
