from flask_babel import gettext as _
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

from app.forms import Form, ValidateUID
from app.models.class_ import Class
from app.models.exam import Exam
from app.models.subject import Subject


class AddExamForm(Form):
    title = StringField(
        _("TITLE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG")),
        ],
    )
    description = TextAreaField(
        _("DESCRIPTION_LABEL"),
        validators=[
            Length(max=50, message=_("THIS_FIELD_CANNOT_EXCEED_50_CHARACTERS_MSG"))
        ],
    )

    exam_date = DateField(
        _("EXAM_DATE_LABEL"), validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))]
    )
    exam_time = TimeField(
        _("EXAM_TIME_LABEL"), validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))]
    )

    total_marks = IntegerField(
        _("TOTAL_MARKS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )
    min_marks = IntegerField(
        _("MINIMUM_MARKS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )

    subject_id = StringField(
        _("SUBJECT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Subject),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Job",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "subjects.html",
        },
    )
    class_id = StringField(
        _("CLASS_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Class),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Class",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "classes.html",
        },
    )

    submit = SubmitField(_("ADD_EXAM_LABEL"))


class UpdateExamForm(AddExamForm):
    uid = HiddenField(
        _("EXAM_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Exam),
        ],
    )
    files = MultipleFileField(
        _("FILES_LABEL"),
        validators=[],
    )
    submit = SubmitField(_("UPDATE_EXAM_LABEL"))
