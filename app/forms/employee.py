from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms.user import AddUserForm, UpdateUserForm


class AddEmployeeForm(AddUserForm):
    job_uid = StringField("Job UID", validators=[Optional(), Length(8, 8)])

    address = StringField("Address", validators=[Length(max=255)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    hire_date = DateField("Hire Date", format="%Y-%m-%d")
    submit = SubmitField("Add")


class UpdateEmployeeForm(UpdateUserForm, AddEmployeeForm):
    uid = HiddenField("Employee UID", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Update")
