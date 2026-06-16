from flask_babel import gettext as _
from wtforms import DecimalField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms import Form, ValidateUID
from app.models.job import Job


class AddJobForm(Form):
    job_title = StringField(
        _("JOB_TITLE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    job_description = TextAreaField(
        _("JOB_DESCRIPTION_LABEL"),
        validators=[
            Optional(),
            Length(max=2000, message=_("THIS_FIELD_CANNOT_EXCEED_2000_CHARACTERS_MSG")),
        ],
    )

    min_salary = DecimalField(
        _("MINIMUM_SALARY_LABEL"),
        places=2,
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            NumberRange(min=0, message=_("VALUE_MUST_BE_AT_LEAST_MIN_S_MSG")),
        ],
    )

    max_salary = DecimalField(
        _("MAXIMUM_SALARY_LABEL"),
        places=2,
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            NumberRange(min=0, message=_("VALUE_MUST_BE_AT_LEAST_MIN_S_MSG")),
        ],
    )

    submit = SubmitField(_("ADD_JOB_LABEL"))


class UpdateJobForm(AddJobForm):
    uid = HiddenField(
        _("JOB_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Job),
        ],
    )

    submit = SubmitField(_("UPDATE_JOB_LABEL"))
