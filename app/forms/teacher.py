import json
import re

from wtforms import DecimalField, HiddenField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.extensions.db import db
from app.forms.user import AddUserForm, UpdateUserForm
from app.func import validate_uid
from app.models.subject import Subject
from app.models.time import Time


class AddTeacherForm(AddUserForm):
    time_id = StringField("Time UID", validators=[DataRequired(), Length(8, 8)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    subjects = StringField("Subject UID", validators=[Optional()])
    submit = SubmitField("Add Teacher")

    def validate_time_id(self, time_id) -> None:
        uid = time_id.data

        if not validate_uid(uid):
            raise ValidationError(f"Not a valid Time UID {uid!r}.")

        if not Time.query.filter_by(uid=uid).first():
            raise ValidationError("Time with the given ID was not found :(")

    def validate_subjects(self, subjects) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        subjects = json.loads(subjects.data)

        for uid in subjects:
            if not pattern.search(uid):
                raise ValidationError(f"Not a valid Subject UID {uid!r}.")

            if not db.session.query(Subject).filter_by(uid=uid).count():
                raise ValidationError("Subject with the given ID was not found :(")


class UpdateTeacherForm(UpdateUserForm, AddTeacherForm):
    uid = HiddenField("Teacher ID", validators=[DataRequired()])
    submit = SubmitField("Update Teacher")
