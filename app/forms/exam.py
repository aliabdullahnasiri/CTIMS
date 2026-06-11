from flask_babel import gettext as _
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

from app.forms import Form


class AddExamForm(Form):
    title = StringField(
        _("Title"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=50, message=_("This field cannot exceed 50 characters.")),
        ],
    )
    description = TextAreaField(
        _("Description"),
        validators=[
            Length(max=50, message=_("This field cannot exceed 50 characters."))
        ],
    )

    exam_date = DateField(
        _("Exam Date"), validators=[DataRequired(message=_("This field is required."))]
    )
    exam_time = TimeField(
        _("Exam Time"), validators=[DataRequired(message=_("This field is required."))]
    )

    total_marks = IntegerField(
        _("Total Marks"),
        validators=[DataRequired(message=_("This field is required."))],
        default=100,
    )
    min_marks = IntegerField(
        _("Minimum Marks"),
        validators=[DataRequired(message=_("This field is required."))],
        default=50,
    )

    subject_id = StringField(
        _("Subject UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )
    class_id = StringField(
        _("Class UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )

    submit = SubmitField(_("Add Exam"))


class UpdateExamForm(AddExamForm):
    uid = HiddenField(
        _("Exam UID"), validators=[DataRequired(message=_("This field is required."))]
    )
    files = MultipleFileField(
        _("Files"),
        validators=[],
    )
    submit = SubmitField(_("Update Exam"))
