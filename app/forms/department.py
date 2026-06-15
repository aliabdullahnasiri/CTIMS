from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, ValidateUID
from app.models.department import Department
from app.models.teacher import Teacher


class AddDepartmentForm(Form):
    name = StringField(
        _("Name"),
        validators=[
            DataRequired(message=_("Name is required.")),
            Length(max=50, message=_("Name cannot exceed 50 characters.")),
        ],
    )

    description = TextAreaField(
        _("Description"),
        validators=[
            Optional(),
            Length(max=255, message=_("Description cannot exceed 255 characters.")),
        ],
    )

    head_of_department = StringField(
        _("HOD UID"),
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
        _("Parent Department UID"),
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

    submit = SubmitField(_("Add Department"))


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField(
        _("UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Department),
        ],
    )

    submit = SubmitField(_("Update Department"))
