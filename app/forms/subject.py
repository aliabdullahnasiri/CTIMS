from flask_babel import gettext as _
from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, ValidateUID
from app.models.semester import Semester
from app.models.subject import Subject


class AddSubjectForm(Form):
    name = StringField(
        _("SUBJECT_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    description = TextAreaField(
        _("SUBJECT_DESCRIPTION_LABEL"),
        validators=[
            Optional(),
            Length(max=2000, message=_("THIS_FIELD_CANNOT_EXCEED_2000_CHARACTERS_MSG")),
        ],
    )
    credit = IntegerField(_("CREDIT_LABEL"), validators=[Optional()])

    semester_uid = StringField(
        _("SEMESTER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Semester),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Semester",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "semesters.html",
        },
    )

    files = MultipleFileField(_("FILES_LABEL"))

    submit = SubmitField(_("ADD_SUBJECT_LABEL"))


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField(
        _("SUBJECT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Subject),
        ],
    )

    submit = SubmitField(_("UPDATE_SUBJECT_LABEL"))
