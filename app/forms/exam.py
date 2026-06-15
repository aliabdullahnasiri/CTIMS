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
        _("Title"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=50, message=_("This field cannot exceed 50 characters.")),
        ],
    )
    description = TextAreaField(
        _("Description"),
        validators=[
            Length(max=50, message=_("This field cannot exceed 50 characters."))
        ],
    )

    exam_date = DateField(
        _("Exam Date"), validators=[DataRequired(message=_("This field is required."))]
    )
    exam_time = TimeField(
        _("Exam Time"), validators=[DataRequired(message=_("This field is required."))]
    )

    total_marks = IntegerField(
        _("Total Marks"),
        validators=[DataRequired(message=_("This field is required."))],
    )
    min_marks = IntegerField(
        _("Minimum Marks"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    subject_id = StringField(
        _("Subject UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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
        _("Class UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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

    submit = SubmitField(_("Add Exam"))


class UpdateExamForm(AddExamForm):
    uid = HiddenField(
        _("Exam UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Exam),
        ],
    )
    files = MultipleFileField(
        _("Files"),
        validators=[],
    )
    submit = SubmitField(_("Update Exam"))
