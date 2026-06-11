import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.models.attendance import AttendanceStatus
from app.models.student import Student


class AddStudentAttendanceForm(FlaskForm):
    student_id = StringField(_("Student UID"), validators=[DataRequired(), Length(8, 8)])
    status = SelectField(
        _("Status"),
        validators=[DataRequired()],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    def validate_student_id(self, student_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(student_id.data):
            raise ValidationError(_("Not a valid Student UID."))
        elif not Student.query.filter_by(uid=student_id.data).first():
            raise ValidationError(_("Student with the given ID was not found :("))

    submit = SubmitField(_("Add Attendance"))
