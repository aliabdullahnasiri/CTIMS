from wtforms import EmailField, Form, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_babel import gettext as _

from app.forms import Form


class LoginForm(Form):
    email = EmailField(
        _("Email"),
        validators=[DataRequired(), Email(message=_("Enter a valid email address"))],
    )
    password = PasswordField(_("Password"), validators=[DataRequired()])
    submit = SubmitField(_("Log In"))
