from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class UpdatePermissionForm(FlaskForm):
    uid = HiddenField("Permission UID", validators=[DataRequired()])

    name = StringField("Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    submit = SubmitField("Update Permission")
