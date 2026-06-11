from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.forms import Form


class AddSemesterForm(Form):
    name = StringField(_("Semester Name"), validators=[DataRequired(), Length(max=255)])

    number = IntegerField(_("Semester Number"), validators=[DataRequired()])

    department_uid = StringField(_("Department UID"), validators=[DataRequired()])

    submit = SubmitField(_("Add Semester"))


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField(_("Semester UID"), validators=[DataRequired()])

    submit = SubmitField(_("Update Semester"))
