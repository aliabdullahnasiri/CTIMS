from flask_wtf.file import FileField
from wtforms import (
    DateField,
    FileField,
    HiddenField,
    MultipleFileField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional

from app.forms import Form


class AddUserForm(Form):
    first_name = StringField("First Name", validators=[Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[Length(max=50)])
    user_name = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField("Upload new profile picture.")

    files = MultipleFileField("Files")
    phones = StringField("Phone", validators=[Optional()])
    roles = StringField("Roles", validators=[Optional()])

    submit = SubmitField("Add")


class UpdateUserForm(AddUserForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    password = PasswordField("Password", validators=[Optional()])

    submit = SubmitField("Update")
