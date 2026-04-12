import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.attendance import AttendanceStatus
from app.models.teacher import Teacher


class AddTeacherAttendanceForm(FlaskForm):
    teacher_id = StringField("Teacher UID", validators=[DataRequired(), Length(8, 8)])
    status = SelectField(
        "Status",
        validators=[DataRequired()],
        choices=[AttendanceStatus.ABSENT.value, AttendanceStatus.PRESENT.value],
        default=AttendanceStatus.PRESENT.value,
    )

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^T.\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError("Not a valid Teacher UID.")
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError("Teacher with the given ID was not found :(")

    submit = SubmitField("Add Attendance")
