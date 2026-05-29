from wtforms import PasswordField, SubmitField
from wtforms.validators import Optional

from app.forms.user import AddUserForm


class UpdateProfileForm(AddUserForm):
    password = PasswordField("Password", validators=[Optional()])
    submit = SubmitField("Update")
