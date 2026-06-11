from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddClassForm(Form):
    cls_name = StringField(
        _("Class Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )
    teacher_id = StringField(
        _("Teacher UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )
    semester_id = StringField(
        _("Semester UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )
    time_id = StringField(
        _("Time UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )

    submit = SubmitField(_("Add Class"))


class UpdateClassForm(AddClassForm):
    uid = HiddenField(
        _("Class UID"), validators=[DataRequired(message=_("This field is required."))]
    )

    submit = SubmitField(_("Update Class"))
