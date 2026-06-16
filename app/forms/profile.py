from flask_babel import gettext as _
from wtforms import PasswordField, SubmitField
from wtforms.validators import Optional

from app.forms.user import AddUserForm


class UpdateProfileForm(AddUserForm):
    password = PasswordField(_("PASSWORD_LABEL"), validators=[Optional()])
    submit = SubmitField(_("UPDATE_LABEL"))
