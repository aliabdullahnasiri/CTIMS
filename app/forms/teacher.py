from flask_babel import gettext as _
from wtforms import DecimalField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms import ValidateUID
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.teacher import Teacher
from app.models.time import Time
from app.models.user import User


class AddTeacherForm(AddUserForm):
    time_id = StringField(
        _("TIME_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Time),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Time",
            "data-select-val": "uid",
            "data-search-col": "title",
            "data-template": "times.html",
        },
    )
    salary = DecimalField(
        _("SALARY_LABEL"),
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message=_("VALUE_MUST_BE_AT_LEAST_MIN_S_MSG")),
        ],
    )
    subjects = StringField(_("SUBJECT_UID_LABEL"), validators=[Optional()])
    submit = SubmitField(_("ADD_TEACHER_LABEL"))


class UpdateTeacherForm(UpdateUserForm, AddTeacherForm):
    uid = HiddenField(
        _("TEACHER_ID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Teacher),
        ],
    )
    user_uid = HiddenField(
        _("USER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(User),
        ],
    )
    submit = SubmitField(_("UPDATE_TEACHER_LABEL"))
