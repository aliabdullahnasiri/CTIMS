from wtforms import DecimalField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_babel import gettext as _

from app.forms import Form


class AddJobForm(Form):
    job_title = StringField(_("Job Title"), validators=[DataRequired(), Length(max=255)])

    job_description = TextAreaField(
        _("Job Description"), validators=[Optional(), Length(max=2000)]
    )

    min_salary = DecimalField(
        _("Minimum Salary"), places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    max_salary = DecimalField(
        _("Maximum Salary"), places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    submit = SubmitField(_("Add Job"))


class UpdateJobForm(AddJobForm):
    uid = HiddenField(_("Job UID"), validators=[DataRequired()])

    submit = SubmitField(_("Update Job"))
