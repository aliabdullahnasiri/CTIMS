import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.semester import Semester
from app.models.teacher import Teacher


class AddClassForm(FlaskForm):
    name = StringField("Class Name", validators=[DataRequired(), Length(max=255)])
    teacher_id = StringField("Teacher UID", validators=[DataRequired(), Length(8, 8)])
    semester_id = StringField("Semester UID", validators=[DataRequired(), Length(8, 8)])

    submit = SubmitField("Add Class")

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError("Not a valid Teacher UID.")
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError("Teacher with the given ID was not found :(")

    def validate_semester_id(self, semester_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(semester_id.data):
            raise ValidationError("Not a valid Semester UID.")
        elif not Semester.query.filter_by(uid=semester_id.data).first():
            raise ValidationError("Semester with the given ID was not found :(")


class UpdateClassForm(AddClassForm):
    uid = HiddenField("Class UID", validators=[DataRequired()])

    submit = SubmitField("Update Class")
