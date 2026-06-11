from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class UpdatePermissionForm(Form):
    uid = HiddenField(
        _("Permission UID"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    name = StringField(
        _("Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    description = TextAreaField(
        _("Description"),
        validators=[
            Optional(),
            Length(max=2500, message=_("This field cannot exceed 2500 characters.")),
        ],
    )

    submit = SubmitField(_("Update Permission"))
