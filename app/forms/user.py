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
from flask_babel import gettext as _

from app.forms import Form


class AddUserForm(Form):
    first_name = StringField(_("First Name"), validators=[Length(max=50)])
    middle_name = StringField(_("Middle Name"), validators=[Length(max=50)])
    last_name = StringField(_("Last Name"), validators=[Length(max=50)])
    user_name = StringField(_("Username"), validators=[DataRequired(), Length(max=50)])
    email = StringField(
        _("Email"),
        validators=[DataRequired(), Email(message=_("Enter a valid email address"))],
    )
    password = PasswordField(_("Password"), validators=[DataRequired()])
    birthday = DateField(_("Birthday"), format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField(_("Upload new profile picture."))

    files = MultipleFileField(_("Files"))
    phones = StringField(_("Phone"), validators=[Optional()])
    roles = StringField(_("Roles"), validators=[Optional()])

    submit = SubmitField(_("Add"))


class UpdateUserForm(AddUserForm):
    uid = HiddenField(_("UID"), validators=[DataRequired()])

    password = PasswordField(_("Password"), validators=[Optional()])

    submit = SubmitField(_("Update"))
