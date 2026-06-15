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
        _("Class Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
            MustBeUnique(Class, "name"),
        ],
    )
    teacher_id = StringField(
        _("Teacher UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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
        _("Semester UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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
        _("Time UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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

    submit = SubmitField(_("Add Class"))


class UpdateClassForm(AddClassForm):
    uid = HiddenField(
        _("Class UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Class),
        ],
    )

    submit = SubmitField(_("Update Class"))
