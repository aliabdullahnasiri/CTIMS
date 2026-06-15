import re

from flask_babel import gettext as _
from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length

from app.forms import Form, ValidateUID
from app.models.exam import Exam
from app.models.result import Result
from app.models.student import Student


class AddResultForm(Form):
    exam_id = StringField(
        _("Exam UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Exam),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Exam",
            "data-select-val": "uid",
            "data-search-col": "title",
            "data-template": "classes.html",
        },
    )
    student_id = StringField(
        _("Student UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Student),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Student",
            "data-select-val": "uid",
            "data-search-col": "uid",
            "data-template": "students.html",
        },
    )
    obtained_marks = IntegerField(
        _("Obtained Marks"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    def validate_obtained_marks(self, obtained_marks) -> None:
        if uid := self.exam_id.data:
            exam = Exam.query.filter_by(uid=uid).first()

            if exam and not 0 <= obtained_marks.data <= exam.total_marks:
                raise ValidationError(
                    _("The obtained marks should be between 0 and %s.")
                    % (exam.total_marks)
                )

    submit = SubmitField(_("Add Result"))


class UpdateResultForm(AddResultForm):
    uid = HiddenField(
        _("Result UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Result),
        ],
    )
    files = MultipleFileField(
        _("Files"),
        validators=[],
    )
    submit = SubmitField(_("Update Result"))
