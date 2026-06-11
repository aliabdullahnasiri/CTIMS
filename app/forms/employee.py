from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_babel import gettext as _

from app.forms.user import AddUserForm, UpdateUserForm


class AddEmployeeForm(AddUserForm):
    job_uid = StringField(_("Job UID"), validators=[Optional(), Length(min=8, max=8, message=_("This field must be 8 characters."))])

    address = StringField(_("Address"), validators=[Length(max=255, message=_("This field cannot exceed 255 characters."))])
    salary = DecimalField(
        _("Salary"), places=2, validators=[Optional(), NumberRange(min=0, message=_("Value must be at least %(min)s."))]
    )
    hire_date = DateField(_("Hire Date"), format="%Y-%m-%d")
    submit = SubmitField(_("Add"))


class UpdateEmployeeForm(UpdateUserForm, AddEmployeeForm):
    uid = HiddenField(_("Employee UID"), validators=[DataRequired(message=_("This field is required."))])
    password = PasswordField(_("Password"))
    submit = SubmitField(_("Update"))
