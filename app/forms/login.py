from flask_babel import gettext as _
from wtforms import EmailField, Form, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.forms import Form


class LoginForm(Form):
    email = EmailField(
        _("Email"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Email(message=_("Enter a valid email address")),
        ],
    )
    password = PasswordField(
        _("Password"), validators=[DataRequired(message=_("This field is required."))]
    )
    submit = SubmitField(_("Log In"))
