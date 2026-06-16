from flask_babel import gettext as _
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms import Form, MustBeUnique
from app.models.user import User


class SignupForm(Form):
    user_name = StringField(
        _("USERNAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG")),
            MustBeUnique(User, "user_name", _("USERNAME_ALREADY_TAKEN_MSG")),
        ],
    )
    email = EmailField(
        _("EMAIL_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Email(message=_("ENTER_A_VALID_EMAIL_ADDRESS_PLACEHOLDER")),
            MustBeUnique(User, "email", _("EMAIL_ALREADY_REGISTERED_MSG")),
        ],
    )
    password = PasswordField(
        _("PASSWORD_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=6, message=_("THIS_FIELD_MUST_BE_AT_LEAST_6_CHARACTERS_MSG")),
        ],
    )
    confirm_password = PasswordField(
        _("CONFIRM_PASSWORD_WARNING"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            EqualTo("password", message=_("PASSWORDS_MUST_MATCH_MSG")),
        ],
    )
    submit = SubmitField(_("SIGN_UP_LABEL"))
