from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ReadOnly

from app.forms import Form


class AddRoleForm(Form):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField(
        "Default Role (assigned automatically to new users)",
        default=False,
        validators=[Optional()],
    )

    permissions = StringField("Permissions", validators=[Optional()])

    submit = SubmitField("Add Role")


class UpdateRoleForm(AddRoleForm):
    uid = HiddenField("Role UID", validators=[DataRequired()])
    name = StringField("Name", validators=[ReadOnly(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField("Default", default=False, validators=[Optional()])
    permissions = StringField("Permissions", validators=[Optional()])

    submit = SubmitField("Update Role")
