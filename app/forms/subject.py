from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddSubjectForm(Form):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Subject Description", validators=[Optional(), Length(max=2000)]
    )
    credit = IntegerField("Credit", validators=[Optional()])

    semester_uid = StringField("Semester UID", validators=[DataRequired()])

    files = MultipleFileField("Files")

    submit = SubmitField("Add Subject")


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField("Subject UID", validators=[DataRequired()])

    submit = SubmitField("Update Subject")
