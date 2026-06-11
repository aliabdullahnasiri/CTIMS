from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_babel import gettext as _

from app.forms import Form


class SignupForm(Form):
    user_name = StringField(_("Username"), validators=[DataRequired(), Length(max=50)])
    email = EmailField(_("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_("Password"), validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        _("Confirm Password"),
        validators=[
            DataRequired(),
            EqualTo("password", message=_("Passwords must match")),
        ],
    )
    submit = SubmitField(_("Sign Up"))
