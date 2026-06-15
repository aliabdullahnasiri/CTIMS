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
        _("Time UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
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
        _("Salary"),
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message=_("Value must be at least %(min)s.")),
        ],
    )
    subjects = StringField(_("Subject UID"), validators=[Optional()])
    submit = SubmitField(_("Add Teacher"))


class UpdateTeacherForm(UpdateUserForm, AddTeacherForm):
    uid = HiddenField(
        _("Teacher ID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Teacher),
        ],
    )
    user_uid = HiddenField(
        _("User UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(User),
        ],
    )
    submit = SubmitField(_("Update Teacher"))
