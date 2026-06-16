import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.models.attendance import AttendanceStatus
from app.models.teacher import Teacher


class AddTeacherAttendanceForm(FlaskForm):
    teacher_id = StringField(_("TEACHER_UID_LABEL"), validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")), Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG"))])
    status = SelectField(
        _("STATUS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^T.\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError(_("NOT_A_VALID_TEACHER_UID_MSG"))
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError(_("TEACHER_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"))

    submit = SubmitField(_("ADD_ATTENDANCE_LABEL"))
