from wtforms import DecimalField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.forms.user import AddUserForm, UpdateUserForm


class AddTeacherForm(AddUserForm):
    time_id = StringField("Time UID", validators=[DataRequired(), Length(8, 8)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    subjects = StringField("Subject UID", validators=[Optional()])
    submit = SubmitField("Add Teacher")


class UpdateTeacherForm(UpdateUserForm, AddTeacherForm):
    uid = HiddenField("Teacher ID", validators=[DataRequired()])
    submit = SubmitField("Update Teacher")
