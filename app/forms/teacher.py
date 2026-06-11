from wtforms import DecimalField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_babel import gettext as _

from app.forms.user import AddUserForm, UpdateUserForm


class AddTeacherForm(AddUserForm):
    time_id = StringField(_("Time UID"), validators=[DataRequired(), Length(8, 8)])
    salary = DecimalField(
        _("Salary"), places=2, validators=[Optional(), NumberRange(min=0)]
    )
    subjects = StringField(_("Subject UID"), validators=[Optional()])
    submit = SubmitField(_("Add Teacher"))


class UpdateTeacherForm(UpdateUserForm, AddTeacherForm):
    uid = HiddenField(_("Teacher ID"), validators=[DataRequired()])
    submit = SubmitField(_("Update Teacher"))
