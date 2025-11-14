from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    HiddenField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Subject Description", validators=[Optional(), Length(max=2000)]
    )

    files = MultipleFileField(
        "Files",
        validators=[FileAllowed(["pdf"], "PDF only!")],
    )

    submit = SubmitField("Add Subject")


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField("Subject UID", validators=[DataRequired()])

    submit = SubmitField("Update Subject")
