from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, ValidateUID
from app.models.time import Time


class AddTimeForm(Form):
    """Form to add a new Time record."""

    title = StringField(
        _("TITLE_LABEL"),
        validators=[
            DataRequired(message=_("TITLE_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("TITLE_CANNOT_EXCEED_50_CHARACTERS_MSG")),
        ],
    )

    description = TextAreaField(
        _("DESCRIPTION_LABEL"),
        validators=[
            Optional(),
            Length(max=255, message=_("DESCRIPTION_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    start = TimeField(
        _("START_TIME_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
        format="%H:%M",
    )

    end = TimeField(
        _("END_TIME_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
        format="%H:%M",
    )

    submit = SubmitField(_("ADD_TIME_LABEL"))


class UpdateTimeForm(AddTimeForm):
    """Form to update an existing Time record."""

    uid = HiddenField(
        _("UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Time),
        ],
    )

    submit = SubmitField(_("UPDATE_TIME_LABEL"))
