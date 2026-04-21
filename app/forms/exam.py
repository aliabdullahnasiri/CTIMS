from wtforms import (
    DateField,
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddExamForm(Form):
    title = StringField("Title", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[Length(max=50)])

    exam_date = DateField("Exam Date", validators=[DataRequired()])
    exam_time = TimeField("Exam Time", validators=[DataRequired()])

    total_marks = IntegerField("Total Marks", validators=[DataRequired()], default=100)
    min_marks = IntegerField("Minimum Marks", validators=[DataRequired()], default=50)

    subject_id = StringField("Subject UID", validators=[DataRequired(), Length(8, 8)])
    class_id = StringField("Class UID", validators=[DataRequired(), Length(8, 8)])

    submit = SubmitField("Add Exam")


class UpdateExamForm(AddExamForm):
    uid = HiddenField("Exam UID", validators=[DataRequired()])
    files = MultipleFileField(
        "Files",
        validators=[],
    )
    submit = SubmitField("Update Exam")
