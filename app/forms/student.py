from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import ValidateUID
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.class_ import Class
from app.models.student import Student
from app.models.user import User


class AddStudentForm(AddUserForm):
    submit = SubmitField(_("ADD_LABEL"))


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField(
        _("STUDENT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Student),
        ],
    )
    user_uid = HiddenField(
        _("USER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(User),
        ],
    )
    class_id = StringField(
        _("CLASS_UID_LABEL"),
        validators=[
            Length(8, 8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Class),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Class",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "classes.html",
        },
    )
    submit = SubmitField(_("UPDATE_STUDENT_LABEL"))
