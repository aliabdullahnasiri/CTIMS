from flask_babel import gettext as _
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form, ValidateUID
from app.models.attendance import AttendanceStatus
from app.models.student import Student


class AddStudentAttendanceForm(Form):
    student_id = StringField(
        _("STUDENT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(min=8, max=8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Student),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Student",
            "data-select-val": "uid",
            "data-search-col": "uid",
            "data-template": "students.html",
        },
    )
    status = SelectField(
        _("STATUS_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    submit = SubmitField(_("ADD_ATTENDANCE_LABEL"))
