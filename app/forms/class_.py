from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form, MustBeUnique, ValidateUID
from app.models.class_ import Class
from app.models.semester import Semester
from app.models.teacher import Teacher
from app.models.time import Time


class AddClassForm(Form):
    cls_name = StringField(
        _("Class Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
            MustBeUnique(Class, "name"),
        ],
    )
    teacher_id = StringField(
        _("Teacher UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Teacher),
        ],
    )
    semester_id = StringField(
        _("Semester UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Semester),
        ],
    )
    time_id = StringField(
        _("Time UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
            ValidateUID(Time),
        ],
    )

    submit = SubmitField(_("Add Class"))


class UpdateClassForm(AddClassForm):
    uid = HiddenField(
        _("Class UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Class),
        ],
    )

    submit = SubmitField(_("Update Class"))
