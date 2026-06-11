from flask_babel import gettext as _
from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddRoleForm(Form):
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
            Length(max=2500, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    default = BooleanField(
        _("Default Role (assigned automatically to new users)"),
        default=False,
        validators=[Optional()],
    )

    permissions = StringField(_("Permissions"), validators=[Optional()])

    submit = SubmitField(_("Add Role"))


class UpdateRoleForm(AddRoleForm):
    uid = HiddenField(
        _("Role UID"), validators=[DataRequired(message=_("This field is required."))]
    )
    name = StringField(
        _("Name"),
        validators=[
            Optional(),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    submit = SubmitField(_("Update Role"))
