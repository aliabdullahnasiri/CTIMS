from wtforms import (
    DateField,
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

from app.forms import Form


class AddExamForm(Form):
    title = StringField(_("Title"), validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(_("Description"), validators=[Length(max=50)])

    exam_date = DateField(_("Exam Date"), validators=[DataRequired()])
    exam_time = TimeField(_("Exam Time"), validators=[DataRequired()])

    total_marks = IntegerField(_("Total Marks"), validators=[DataRequired()], default=100)
    min_marks = IntegerField(_("Minimum Marks"), validators=[DataRequired()], default=50)

    subject_id = StringField(_("Subject UID"), validators=[DataRequired(), Length(8, 8)])
    class_id = StringField(_("Class UID"), validators=[DataRequired(), Length(8, 8)])

    submit = SubmitField(_("Add Exam"))


class UpdateExamForm(AddExamForm):
    uid = HiddenField(_("Exam UID"), validators=[DataRequired()])
    files = MultipleFileField(
        _("Files"),
        validators=[],
    )
    submit = SubmitField(_("Update Exam"))
