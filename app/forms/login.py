from wtforms import EmailField, Form, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.forms import Form


class LoginForm(Form):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
