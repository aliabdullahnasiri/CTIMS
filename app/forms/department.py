from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddDepartmentForm(Form):
    name = StringField(
        _("Name"),
        validators=[
            DataRequired(message=_("Name is required.")),
            Length(max=50, message=_("Name cannot exceed 50 characters.")),
        ],
    )

    description = TextAreaField(
        _("Description"),
        validators=[
            Optional(),
            Length(max=255, message=_("Description cannot exceed 255 characters.")),
        ],
    )

    head_of_department = StringField(
        _("HOD UID"),
        validators=[
            Optional(),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )

    parent_department_uid = StringField(
        _("Parent Department UID"),
        validators=[
            Optional(),
            Length(min=8, max=8, message=_("This field must be 8 characters.")),
        ],
    )

    submit = SubmitField(_("Add Department"))


class UpdateDepartmentForm(AddDepartmentForm):
    """Form to update an existing Department record."""

    uid = HiddenField(_("UID"))

    submit = SubmitField(_("Update Department"))
