from flask_babel import gettext as _
from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddSemesterForm(Form):
    name = StringField(
        _("Semester Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    number = IntegerField(
        _("Semester Number"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    department_uid = StringField(
        _("Department UID"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    submit = SubmitField(_("Add Semester"))


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField(
        _("Semester UID"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    submit = SubmitField(_("Update Semester"))
