from wtforms import PasswordField, SubmitField
from wtforms.validators import Optional
from flask_babel import gettext as _

from app.forms.user import AddUserForm


class UpdateProfileForm(AddUserForm):
    password = PasswordField(_("Password"), validators=[Optional()])
    submit = SubmitField(_("Update"))
