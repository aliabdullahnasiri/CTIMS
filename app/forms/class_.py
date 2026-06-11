from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form


class AddClassForm(Form):
    cls_name = StringField(_("Class Name"), validators=[DataRequired(), Length(max=255)])
    teacher_id = StringField(_("Teacher UID"), validators=[DataRequired(), Length(8, 8)])
    semester_id = StringField(_("Semester UID"), validators=[DataRequired(), Length(8, 8)])
    time_id = StringField(_("Time UID"), validators=[DataRequired(), Length(8, 8)])

    submit = SubmitField(_("Add Class"))


class UpdateClassForm(AddClassForm):
    uid = HiddenField(_("Class UID"), validators=[DataRequired()])

    submit = SubmitField(_("Update Class"))
