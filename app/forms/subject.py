from flask_babel import gettext as _
from wtforms import (
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddSubjectForm(Form):
    name = StringField(
        _("Subject Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    description = TextAreaField(
        _("Subject Description"),
        validators=[
            Optional(),
            Length(max=2000, message=_("This field cannot exceed 2000 characters.")),
        ],
    )
    credit = IntegerField(_("Credit"), validators=[Optional()])

    semester_uid = StringField(
        _("Semester UID"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    files = MultipleFileField(_("Files"))

    submit = SubmitField(_("Add Subject"))


class UpdateSubjectForm(AddSubjectForm):
    uid = HiddenField(
        _("Subject UID"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    submit = SubmitField(_("Update Subject"))
