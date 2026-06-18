from flask_babel import gettext as _
from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, MustBeUnique, ValidateUID
from app.models.permission import Permission
from app.models.role import Role


class AddRoleForm(Form):
    name = StringField(
        _("NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
            MustBeUnique(Role, "name"),
        ],
    )

    description = TextAreaField(
        _("DESCRIPTION_LABEL"),
        validators=[
            Optional(),
            Length(max=2500, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    default = BooleanField(
        _("DEFAULT_ROLE_ASSIGNED_AUTOMATICALLY_TO_NEW_USERS_MSG"),
        default=False,
        validators=[Optional()],
    )

    permissions = StringField(
        _("PERMISSIONS_LABEL"),
        validators=[Optional(), ValidateUID(Permission)],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Permission",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "roles.html",
        },
    )

    submit = SubmitField(_("ADD_ROLE_LABEL"))


class UpdateRoleForm(AddRoleForm):
    uid = HiddenField(
        _("ROLE_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Role),
        ],
    )
    name = StringField(
        _("NAME_LABEL"),
        validators=[
            Optional(),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    submit = SubmitField(_("UPDATE_ROLE_LABEL"))
