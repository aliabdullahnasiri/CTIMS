from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form, MustBeUnique, ValidateUID
from app.models.class_ import Class
from app.models.semester import Semester
from app.models.teacher import Teacher
from app.models.time import Time


class AddClassForm(Form):
    cls_name = StringField(
        _("CLASS_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
            MustBeUnique(Class, "name"),
        ],
    )
    teacher_id = StringField(
        _("TEACHER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Teacher),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Teacher",
            "data-select-val": "uid",
            "data-search-col": "uid",
            "data-template": "teachers.html",
        },
    )
    semester_id = StringField(
        _("SEMESTER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
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
    time_id = StringField(
        _("TIME_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Time),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Time",
            "data-select-val": "uid",
            "data-search-col": "title",
            "data-template": "times.html",
        },
    )

    submit = SubmitField(_("ADD_CLASS_LABEL"))


class UpdateClassForm(AddClassForm):
    uid = HiddenField(
        _("CLASS_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Class),
        ],
    )

    submit = SubmitField(_("UPDATE_CLASS_LABEL"))
