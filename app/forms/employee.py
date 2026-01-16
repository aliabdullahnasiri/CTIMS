import json
import re

from sqlalchemy import and_
from wtforms import (
    DateField,
    DecimalField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from app.extensions import db
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.employee import Employee
from app.models.job import Job
from app.models.phone import EmployeePhone


class AddEmployeeForm(AddUserForm):
    address = StringField("Address", validators=[Length(max=255)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    hire_date = DateField("Hire Date", format="%Y-%m-%d")
    job_uid = StringField("Job UID", validators=[Optional(), Length(8, 8)])
    phones = StringField("Phone", validators=[Optional()])
    submit = SubmitField("Add")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(EmployeePhone)
                .filter(
                    EmployeePhone.phone_number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")

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

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        if hasattr(self, "uid"):
            uid = self.uid.data

            for num in nums:
                if (
                    db.session.query(EmployeePhone)
                    .filter(
                        and_(
                            EmployeePhone.employee_id != uid,
                            EmployeePhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")

    def validate_user_name(self, user_name, uid=None):
        return super().validate_user_name(
            user_name,
            (
                employee.user.uid
                if (
                    employee := db.session.query(Employee)
                    .filter_by(uid=self.uid.data)
                    .first()
                )
                else uid
            ),
        )

    def validate_email(self, email, uid=None):
        return super().validate_email(
            email,
            (
                employee.user.uid
                if (
                    employee := db.session.query(Employee)
                    .filter_by(uid=self.uid.data)
                    .first()
                )
                else uid
            ),
        )
