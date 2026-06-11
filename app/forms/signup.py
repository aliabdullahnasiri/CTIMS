from flask_babel import gettext as _
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms import Form


class SignupForm(Form):
    user_name = StringField(
        _("Username"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=50, message=_("This field cannot exceed 50 characters.")),
        ],
    )
    email = EmailField(
        _("Email"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Email(message=_("Enter a valid email address")),
        ],
    )
    password = PasswordField(
        _("Password"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=6, message=_("This field must be at least 6 characters.")),
        ],
    )
    confirm_password = PasswordField(
        _("Confirm Password"),
        validators=[
            DataRequired(message=_("This field is required.")),
            EqualTo("password", message=_("Passwords must match")),
        ],
    )
    submit = SubmitField(_("Sign Up"))
