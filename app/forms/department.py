from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, ValidateUID
from app.models.department import Department
from app.models.teacher import Teacher


class AddDepartmentForm(Form):
    name = StringField(
        _("NAME_LABEL"),
        validators=[
            DataRequired(message=_("NAME_IS_REQUIRED_ERROR")),
            Length(max=50, message=_("NAME_CANNOT_EXCEED_50_CHARACTERS_MSG")),
        ],
    )

    description = TextAreaField(
        _("DESCRIPTION_LABEL"),
        validators=[
            Optional(),
            Length(max=255, message=_("DESCRIPTION_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    head_of_department = StringField(
        _("HOD_UID_LABEL"),
        validators=[
            Optional(),
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

    parent_department_uid = StringField(
        _("PARENT_DEPARTMENT_UID_MSG"),
        validators=[
            ValidateUID(Department),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Department",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "departments.html",
        },
    )

    submit = SubmitField(_("ADD_DEPARTMENT_LABEL"))


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField(
        _("UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Department),
        ],
    )

    submit = SubmitField(_("UPDATE_DEPARTMENT_LABEL"))
