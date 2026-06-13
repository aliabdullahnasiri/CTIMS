from flask_babel import gettext as _
from wtforms import DecimalField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms import Form, ValidateUID
from app.models.job import Job


class AddJobForm(Form):
    job_title = StringField(
        _("Job Title"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    job_description = TextAreaField(
        _("Job Description"),
        validators=[
            Optional(),
            Length(max=2000, message=_("This field cannot exceed 2000 characters.")),
        ],
    )

    min_salary = DecimalField(
        _("Minimum Salary"),
        places=2,
        validators=[
            DataRequired(message=_("This field is required.")),
            NumberRange(min=0, message=_("Value must be at least %(min)s.")),
        ],
    )

    max_salary = DecimalField(
        _("Maximum Salary"),
        places=2,
        validators=[
            DataRequired(message=_("This field is required.")),
            NumberRange(min=0, message=_("Value must be at least %(min)s.")),
        ],
    )

    submit = SubmitField(_("Add Job"))


class UpdateJobForm(AddJobForm):
    uid = HiddenField(
        _("Job UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Job),
        ],
    )

    submit = SubmitField(_("Update Job"))
