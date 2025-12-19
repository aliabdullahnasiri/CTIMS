import re

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length

from app.models.exam import Exam
from app.models.student import Student


class AddResultForm(FlaskForm):
    exam_id = StringField("Exam UID", validators=[DataRequired(), Length(8, 8)])
    student_id = StringField("Student UID", validators=[DataRequired(), Length(8, 8)])
    obtained_marks = IntegerField("Obtained Marks", validators=[DataRequired()])

    def validate_obtained_marks(self, obtained_marks) -> None:
        if uid := self.exam_id.data:
            exam = Exam.query.filter_by(uid=uid).first()

            if exam and not 0 <= obtained_marks.data <= exam.total_marks:
                raise ValidationError(
                    "The obtained marks should be between 0 and %s."
                    % (exam.total_marks)
                )

    def validate_exam_id(self, exam_id) -> None:
        pattern: re.Pattern = re.compile(r"^E.\d{6}$")

        if not pattern.search(exam_id.data):
            raise ValidationError("Not a valid Exam UID.")
        elif not Exam.query.filter_by(uid=exam_id.data).first():
            raise ValidationError("Exam with the given ID was not found :(")

    def validate_student_id(self, student_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(student_id.data):
            raise ValidationError("Not a valid Student UID.")
        elif not Student.query.filter_by(uid=student_id.data).first():
            raise ValidationError("Student with the given ID was not found :(")

    submit = SubmitField("Add Result")


class UpdateResultForm(AddResultForm):
    uid = HiddenField("Result UID", validators=[DataRequired()])
    files = MultipleFileField(
        "Files",
        validators=[],
    )
    submit = SubmitField("Update Result")
