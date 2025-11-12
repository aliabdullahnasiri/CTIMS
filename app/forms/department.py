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

    manager = StringField(
        "Manager UID",
        validators=[Optional(), Length(min=8, max=8)],
    )

    submit = SubmitField("Add Department")

    def validate_manager(self, manager):
        if not Employee.query.filter_by(uid=manager.data).first():
            raise ValidationError("Employee with the given ID was not found :(")


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField("UID")

    submit = SubmitField("Update Department")
