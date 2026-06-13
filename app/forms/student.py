from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import ValidateUID
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.class_ import Class
from app.models.student import Student


class AddStudentForm(AddUserForm):
    submit = SubmitField(_("Add"))


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField(
        _("Student UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Student),
        ],
    )
    class_id = StringField(
        _("Class UID"),
        validators=[
            Length(8, 8, message=_("This field must be 8 characters.")),
            ValidateUID(Class),
        ],
    )
    submit = SubmitField(_("Update Student"))
