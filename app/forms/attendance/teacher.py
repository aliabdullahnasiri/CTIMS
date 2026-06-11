import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.models.attendance import AttendanceStatus
from app.models.teacher import Teacher


class AddTeacherAttendanceForm(FlaskForm):
    teacher_id = StringField(_("Teacher UID"), validators=[DataRequired(message=_("This field is required.")), Length(min=8, max=8, message=_("This field must be 8 characters."))])
    status = SelectField(
        _("Status"),
        validators=[DataRequired(message=_("This field is required."))],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^T.\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError(_("Not a valid Teacher UID."))
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError(_("Teacher with the given ID was not found :("))

    submit = SubmitField(_("Add Attendance"))
