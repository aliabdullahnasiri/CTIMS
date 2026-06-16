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
        _("JOB_UID_LABEL"),
        validators=[
            Optional(),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
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
        _("ADDRESS_LABEL"),
        validators=[
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG"))
        ],
    )
    salary = DecimalField(
        _("SALARY_LABEL"),
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message=_("VALUE_MUST_BE_AT_LEAST_MIN_S_MSG")),
        ],
    )
    hire_date = DateField(_("HIRE_DATE_LABEL"), format="%Y-%m-%d")
    submit = SubmitField(_("ADD_LABEL"))


class UpdateEmployeeForm(UpdateUserForm, AddEmployeeForm):
    uid = HiddenField(
        _("EMPLOYEE_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Employee),
        ],
    )
    user_uid = HiddenField(
        _("USER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(User),
        ],
    )
    password = PasswordField(_("PASSWORD_LABEL"))
    submit = SubmitField(_("UPDATE_LABEL"))
