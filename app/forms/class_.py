import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from app.models.teacher import Teacher


class AddClassForm(FlaskForm):
    name = StringField("Class Name", validators=[DataRequired(), Length(max=255)])
    teacher_id = StringField("Teacher UID", validators=[Length(8, 8)])

    submit = SubmitField("Add Class")

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError("Not a valid Teacher UID.")
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError("Teacher with the given ID was not found :(")


class UpdateClassForm(AddClassForm):
    uid = HiddenField("Class UID", validators=[DataRequired()])

    submit = SubmitField("Update Class")
