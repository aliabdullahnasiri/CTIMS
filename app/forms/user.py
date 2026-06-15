from flask import url_for
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
        _("First Name"),
        validators=[
            Length(max=50, message=_("This field cannot exceed 50 characters."))
        ],
    )
    middle_name = StringField(
        _("Middle Name"),
        validators=[
            Length(max=50, message=_("This field cannot exceed 50 characters."))
        ],
    )
    last_name = StringField(
        _("Last Name"),
        validators=[
            Length(max=50, message=_("This field cannot exceed 50 characters."))
        ],
    )
    user_name = StringField(
        _("Username"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=50, message=_("This field cannot exceed 50 characters.")),
            MustBeUnique(User, "user_name", _("Username already taken")),
        ],
    )
    email = StringField(
        _("Email"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Email(message=_("Enter a valid email address")),
            MustBeUnique(User, "email", _("Email already registered")),
        ],
    )
    password = PasswordField(
        _("Password"), validators=[DataRequired(message=_("This field is required."))]
    )
    birthday = DateField(_("Birthday"), format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField(_("Upload new profile picture."))

    files = MultipleFileField(_("Files"))
    phones = StringField(
        _("Phone"),
        validators=[
            Optional(),
            MustBeUnique(
                Phone,
                "number",
                _("Duplicate entry for phone number!"),
                "user_id",
            ),
        ],
    )
    roles = StringField(
        _("Roles"),
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

    submit = SubmitField(_("Add"))


class UpdateUserForm(AddUserForm):
    uid = HiddenField(
        _("UID"), validators=[DataRequired(message=_("This field is required."))]
    )

    password = PasswordField(_("Password"), validators=[Optional()])

    submit = SubmitField(_("Update"))
