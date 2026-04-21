from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddDepartmentForm(Form):
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

    parent_department_uid = StringField(
        "Parent Department UID",
        validators=[Optional(), Length(min=8, max=8)],
    )

    submit = SubmitField("Add Department")


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField("UID")

    submit = SubmitField("Update Department")
