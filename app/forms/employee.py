from flask_babel import gettext as _
from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms import ValidateUID
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.employee import Employee
from app.models.job import Job
from app.models.user import User


class AddEmployeeForm(AddUserForm):
    job_uid = StringField(
        _("Job UID"),
        validators=[
            Optional(),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Job),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Job",
            "data-select-val": "uid",
            "data-search-col": "job_title",
            "data-template": "jobs.html",
        },
    )

    address = StringField(
        _("Address"),
        validators=[
            Length(max=255, message=_("This field cannot exceed 255 characters."))
        ],
    )
    salary = DecimalField(
        _("Salary"),
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message=_("Value must be at least %(min)s.")),
        ],
    )
    hire_date = DateField(_("Hire Date"), format="%Y-%m-%d")
    submit = SubmitField(_("Add"))


class UpdateEmployeeForm(UpdateUserForm, AddEmployeeForm):
    uid = HiddenField(
        _("Employee UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Employee),
        ],
    )
    user_uid = HiddenField(
        _("User UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(User),
        ],
    )
    password = PasswordField(_("Password"))
    submit = SubmitField(_("Update"))
