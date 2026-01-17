import re

from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms.user import AddUserForm, UpdateUserForm
from app.models.job import Job


class AddEmployeeForm(AddUserForm):
    job_uid = StringField("Job UID", validators=[Optional(), Length(8, 8)])

    address = StringField("Address", validators=[Length(max=255)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    hire_date = DateField("Hire Date", format="%Y-%m-%d")
    submit = SubmitField("Add")

    def validate_job_uid(self, job_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(job_uid.data):
            raise ValidationError("Not a valid Job ID.")
        elif not Job.query.filter_by(uid=job_uid.data).first():
            raise ValidationError("Job with the given ID was not found :(")


class UpdateEmployeeForm(UpdateUserForm, AddEmployeeForm):
    uid = HiddenField("Employee UID", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Update")
