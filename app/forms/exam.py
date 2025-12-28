import re

from flask_wtf import FlaskForm
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
from wtforms.validators import DataRequired, Length, ValidationError

from app.models.class_ import Class
from app.models.subject import Subject


class AddExamForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[Length(max=50)])

    exam_date = DateField("Exam Date", validators=[DataRequired()])
    exam_time = TimeField("Exam Time", validators=[DataRequired()])

    total_marks = IntegerField("Total Marks", validators=[DataRequired()], default=100)
    min_marks = IntegerField("Minimum Marks", validators=[DataRequired()], default=50)

    subject_id = StringField("Subject UID", validators=[DataRequired(), Length(8, 8)])
    class_id = StringField("Class UID", validators=[DataRequired(), Length(8, 8)])

    def validate_subject_id(self, subject_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(subject_id.data):
            raise ValidationError("Not a valid Subject UID.")
        elif not Subject.query.filter_by(uid=subject_id.data).first():
            raise ValidationError("Subject with the given ID was not found :(")

    def validate_class_id(self, class_id) -> None:
        pattern: re.Pattern = re.compile(r"^C.\d{6}$")

        if not pattern.search(class_id.data):
            raise ValidationError("Not a valid Class UID.")
        elif not Class.query.filter_by(uid=class_id.data).first():
            raise ValidationError("Class with the given ID was not found :(")

    submit = SubmitField("Add Exam")


class UpdateExamForm(AddExamForm):
    uid = HiddenField("Exam UID", validators=[DataRequired()])
    files = MultipleFileField(
        "Files",
        validators=[],
    )
    submit = SubmitField("Update Exam")
