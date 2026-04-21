from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms.user import AddUserForm, UpdateUserForm


class AddStudentForm(AddUserForm):
    class_id = StringField("Class UID", validators=[DataRequired(), Length(8, 8)])
    submit = SubmitField("Add")


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField("Student UID", validators=[DataRequired()])
    submit = SubmitField("Update Student")
