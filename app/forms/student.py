from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms.user import AddUserForm, UpdateUserForm


class AddStudentForm(AddUserForm):
    submit = SubmitField("Add")


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField("Student UID", validators=[DataRequired()])
    class_id = StringField("Class UID", validators=[Length(8, 8)])
    submit = SubmitField("Update Student")
