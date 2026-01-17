import re

from wtforms import HiddenField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.forms.user import AddUserForm, UpdateUserForm
from app.models.class_ import Class


class AddStudentForm(AddUserForm):
    class_id = StringField("Class UID", validators=[DataRequired(), Length(8, 8)])
    submit = SubmitField("Add")

    def validate_class_id(self, class_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(class_id.data):
            raise ValidationError("Not a valid Class UID.")
        elif not Class.query.filter_by(uid=class_id.data).first():
            raise ValidationError("Class with the given ID was not found :(")


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField("Student UID", validators=[DataRequired()])
    submit = SubmitField("Update Student")
