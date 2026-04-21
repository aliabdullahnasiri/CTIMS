from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class UpdatePermissionForm(Form):
    uid = HiddenField("Permission UID", validators=[DataRequired()])

    name = StringField("Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    submit = SubmitField("Update Permission")
