from flask_babel import gettext as _
from wtforms import DecimalField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms.user import AddUserForm, UpdateUserForm


class AddTeacherForm(AddUserForm):
    time_id = StringField(
        _("Time UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
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
        _("Teacher ID"), validators=[DataRequired(message=_("This field is required."))]
    )
    submit = SubmitField(_("Update Teacher"))
