from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddSemesterForm(Form):
    name = StringField("Semester Name", validators=[DataRequired(), Length(max=255)])

    number = IntegerField("Semester Number", validators=[DataRequired()])

    department_uid = StringField("Department UID", validators=[DataRequired()])

    submit = SubmitField("Add Semester")


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField("Semester UID", validators=[DataRequired()])

    submit = SubmitField("Update Semester")
