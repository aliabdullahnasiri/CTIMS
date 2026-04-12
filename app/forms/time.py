from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Length, Optional


class AddTimeForm(FlaskForm):
    """Form to add a new Time record."""

    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required."),
            Length(max=50, message="Title cannot exceed 50 characters."),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional(),
            Length(max=255, message="Description cannot exceed 255 characters."),
        ],
    )

    start = TimeField(
        "Start Time",
        validators=[DataRequired()],
        format="%H:%M",
    )

    end = TimeField(
        "End Time",
        validators=[DataRequired()],
        format="%H:%M",
    )

    submit = SubmitField("Add Time")


class UpdateTimeForm(AddTimeForm):
    """Form to update an existing Time record."""

    uid = HiddenField("UID")

    submit = SubmitField("Update Time")
