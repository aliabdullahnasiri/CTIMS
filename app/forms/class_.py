from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddClassForm(Form):
    cls_name = StringField("Class Name", validators=[DataRequired(), Length(max=255)])
    teacher_id = StringField("Teacher UID", validators=[DataRequired(), Length(8, 8)])
    semester_id = StringField("Semester UID", validators=[DataRequired(), Length(8, 8)])
    time_id = StringField("Time UID", validators=[DataRequired(), Length(8, 8)])

    submit = SubmitField("Add Class")


class UpdateClassForm(AddClassForm):
    uid = HiddenField("Class UID", validators=[DataRequired()])

    submit = SubmitField("Update Class")
