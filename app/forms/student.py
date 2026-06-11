from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.forms.user import AddUserForm, UpdateUserForm


class AddStudentForm(AddUserForm):
    submit = SubmitField(_("Add"))


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField(_("Student UID"), validators=[DataRequired()])
    class_id = StringField(_("Class UID"), validators=[Length(8, 8)])
    submit = SubmitField(_("Update Student"))
