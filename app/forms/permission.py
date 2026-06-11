from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from flask_babel import gettext as _

from app.forms import Form


class UpdatePermissionForm(Form):
    uid = HiddenField(_("Permission UID"), validators=[DataRequired()])

    name = StringField(_("Name"), validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        _("Description"), validators=[Optional(), Length(max=2500)]
    )

    submit = SubmitField(_("Update Permission"))
