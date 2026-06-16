from flask_babel import gettext as _
from flask_wtf.file import FileField
from wtforms import (
    DateField,
    FileField,
    HiddenField,
    MultipleFileField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional

from app.forms import Form, MustBeUnique, ValidateUID
from app.models.phone import Phone
from app.models.role import Role
from app.models.user import User


class AddUserForm(Form):
    first_name = StringField(
        _("FIRST_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG")),
        ],
    )
    middle_name = StringField(
        _("MIDDLE_NAME_LABEL"),
        validators=[
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG"))
        ],
    )
    last_name = StringField(
        _("LAST_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG")),
        ],
    )
    user_name = StringField(
        _("USERNAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG")),
            MustBeUnique(User, "user_name", _("USERNAME_ALREADY_TAKEN_MSG")),
        ],
    )
    email = StringField(
        _("EMAIL_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Email(message=_("ENTER_A_VALID_EMAIL_ADDRESS_PLACEHOLDER")),
            MustBeUnique(User, "email", _("EMAIL_ALREADY_REGISTERED_MSG")),
        ],
    )
    password = PasswordField(
        _("PASSWORD_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )
    birthday = DateField(
        _("BIRTHDAY_LABEL"), format="%Y-%m-%d", validators=[Optional()]
    )
    avatar = FileField(_("UPLOAD_NEW_PROFILE_PICTURE_MSG"))

    files = MultipleFileField(_("FILES_LABEL"))
    phones = StringField(
        _("PHONE_LABEL"),
        validators=[
            Optional(),
            MustBeUnique(
                Phone,
                "number",
                _("DUPLICATE_ENTRY_FOR_PHONE_NUMBER_MSG"),
                "user_id",
                format=True,
            ),
        ],
    )
    roles = StringField(
        _("ROLES_LABEL"),
        validators=[Optional(), ValidateUID(Role)],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Role",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "roles.html",
        },
    )

    submit = SubmitField(_("ADD_LABEL"))


class UpdateUserForm(AddUserForm):
    uid = HiddenField(
        _("UID_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )

    password = PasswordField(_("PASSWORD_LABEL"), validators=[Optional()])

    submit = SubmitField(_("UPDATE_LABEL"))
