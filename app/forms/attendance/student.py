import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.models.attendance import AttendanceStatus
from app.models.student import Student


class AddStudentAttendanceForm(FlaskForm):
    student_id = StringField(_("STUDENT_UID_LABEL"), validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")), Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG"))])
    status = SelectField(
        _("STATUS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    def validate_student_id(self, student_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(student_id.data):
            raise ValidationError(_("NOT_A_VALID_STUDENT_UID_MSG"))
        elif not Student.query.filter_by(uid=student_id.data).first():
            raise ValidationError(_("STUDENT_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"))

    submit = SubmitField(_("ADD_ATTENDANCE_LABEL"))
