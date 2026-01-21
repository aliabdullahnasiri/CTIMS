from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class UpdateRoleForm(FlaskForm):
    uid = HiddenField("Role UID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField("Default", default=False, validators=[Optional()])
    permissions = StringField("Permissions", validators=[Optional()])

    submit = SubmitField("Update Role")
