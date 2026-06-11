from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from flask_babel import gettext as _

from app.forms import Form


class AddRoleForm(Form):
    name = StringField(_("Name"), validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        _("Description"), validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField(
        _("Default Role (assigned automatically to new users)"),
        default=False,
        validators=[Optional()],
    )

    permissions = StringField(_("Permissions"), validators=[Optional()])

    submit = SubmitField(_("Add Role"))


class UpdateRoleForm(AddRoleForm):
    uid = HiddenField(_("Role UID"), validators=[DataRequired()])
    name = StringField(_("Name"), validators=[Optional(), Length(max=255)])

    submit = SubmitField(_("Update Role"))
