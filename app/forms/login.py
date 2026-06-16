from flask_babel import gettext as _
from wtforms import EmailField, Form, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.forms import Form


class LoginForm(Form):
    email = EmailField(
        _("EMAIL_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Email(message=_("ENTER_A_VALID_EMAIL_ADDRESS_PLACEHOLDER")),
        ],
    )
    password = PasswordField(
        _("PASSWORD_LABEL"), validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))]
    )
    submit = SubmitField(_("LOG_IN_LABEL"))
