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
        _("EXAM_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Exam),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Exam",
            "data-select-val": "uid",
            "data-search-col": "title",
            "data-template": "exams.html",
        },
    )
    student_id = StringField(
        _("STUDENT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
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
        _("OBTAINED_MARKS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )

    def validate_obtained_marks(self, obtained_marks) -> None:
        if uid := self.exam_id.data:
            exam = Exam.query.filter_by(uid=uid).first()

            if exam and not 0 <= obtained_marks.data <= exam.total_marks:
                raise ValidationError(
                    _("THE_OBTAINED_MARKS_SHOULD_BE_BETWEEN_0_AND_S_MSG")
                    % (exam.total_marks)
                )

    submit = SubmitField(_("ADD_RESULT_LABEL"))


class UpdateResultForm(AddResultForm):
    uid = HiddenField(
        _("RESULT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Result),
        ],
    )
    files = MultipleFileField(
        _("FILES_LABEL"),
        validators=[],
    )
    submit = SubmitField(_("UPDATE_RESULT_LABEL"))
