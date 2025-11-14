import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.department import Department


class AddSemesterForm(FlaskForm):
    name = StringField("Semester Name", validators=[DataRequired(), Length(max=255)])

    number = IntegerField("Semester Number", validators=[DataRequired()])

    department_uid = StringField("Department UID", validators=[DataRequired()])

    submit = SubmitField("Add Semester")

    def validate_department_uid(self, department_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(department_uid.data):
            raise ValidationError("Not a valid Department UID.")
        elif not Department.query.filter_by(uid=department_uid.data).first():
            raise ValidationError("Department with the given ID was not found :(")


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField("Semester UID", validators=[DataRequired()])

    submit = SubmitField("Update Semester")
