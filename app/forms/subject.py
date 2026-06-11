from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional
from flask_babel import gettext as _

from app.forms import Form


class AddSubjectForm(Form):
    name = StringField(_("Subject Name"), validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        _("Subject Description"), validators=[Optional(), Length(max=2000)]
    )
    credit = IntegerField(_("Credit"), validators=[Optional()])

    semester_uid = StringField(_("Semester UID"), validators=[DataRequired()])

    files = MultipleFileField(_("Files"))

    submit = SubmitField(_("Add Subject"))


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField(_("Subject UID"), validators=[DataRequired()])

    submit = SubmitField(_("Update Subject"))
