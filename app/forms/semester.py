from flask_babel import gettext as _
from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form, ValidateUID
from app.models.department import Department
from app.models.semester import Semester


class AddSemesterForm(Form):
    name = StringField(
        _("Semester Name"),
        validators=[
            DataRequired(message=_("This field is required.")),
            Length(max=255, message=_("This field cannot exceed 255 characters.")),
        ],
    )

    number = IntegerField(
        _("Semester Number"),
        validators=[DataRequired(message=_("This field is required."))],
    )

    department_uid = StringField(
        _("Department UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Department),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Department",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "departments.html",
        },
    )

    submit = SubmitField(_("Add Semester"))


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField(
        _("Semester UID"),
        validators=[
            DataRequired(message=_("This field is required.")),
            ValidateUID(Semester),
        ],
    )

    submit = SubmitField(_("Update Semester"))
