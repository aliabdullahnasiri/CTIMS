from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddTimeForm(Form):
    """Form to add a new Time record."""

    title = StringField(
        _("Title"),
        validators=[
            DataRequired(message=_("Title is required.")),
            Length(max=50, message=_("Title cannot exceed 50 characters.")),
        ],
    )

    description = TextAreaField(
        _("Description"),
        validators=[
            Optional(),
            Length(max=255, message=_("Description cannot exceed 255 characters.")),
        ],
    )

    start = TimeField(
        _("Start Time"),
        validators=[DataRequired(message=_("This field is required."))],
        format="%H:%M",
    )

    end = TimeField(
        _("End Time"),
        validators=[DataRequired(message=_("This field is required."))],
        format="%H:%M",
    )

    submit = SubmitField(_("Add Time"))


class UpdateTimeForm(AddTimeForm):
    """Form to update an existing Time record."""

    uid = HiddenField(_("UID"))

    submit = SubmitField(_("Update Time"))
