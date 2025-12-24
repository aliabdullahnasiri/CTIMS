import re

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional, Regexp

from app.models.employee import Employee
from app.models.teacher import Teacher


class AddDepartmentForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Name is required."),
            Length(max=50, message="Name cannot exceed 50 characters."),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional(),
            Length(max=255, message="Description cannot exceed 255 characters."),
        ],
    )

    head_of_department = StringField(
        "HOD UID",
        validators=[Optional(), Length(min=8, max=8)],
    )

    submit = SubmitField("Add Department")

    def validate_head_of_department(self, head_of_department) -> None:
        h: str = head_of_department.data
        pattern: re.Pattern = re.compile(r"^(E|T).\d{6}$")

        if not pattern.search(h):
            raise ValidationError("Not a valid head of department UID.")
        elif h.startswith("E") and not Employee.query.filter_by(uid=h).first():
            raise ValidationError("Employee with the given ID was not found :(")
        elif h.startswith("T") and not Teacher.query.filter_by(uid=h).first():
            raise ValidationError("Teacher with the given ID was not found :(")


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField("UID")

    submit = SubmitField("Update Department")
