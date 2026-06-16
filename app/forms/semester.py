from flask_babel import gettext as _
from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.forms import Form, ValidateUID
from app.models.department import Department
from app.models.semester import Semester


class AddSemesterForm(Form):
    name = StringField(
        _("SEMESTER_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    number = IntegerField(
        _("SEMESTER_NUMBER_LABEL"),
        validators=[DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR"))],
    )

    department_uid = StringField(
        _("DEPARTMENT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
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

    submit = SubmitField(_("ADD_SEMESTER_LABEL"))


class UpdateSemesterForm(AddSemesterForm):
    uid = HiddenField(
        _("SEMESTER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Semester),
        ],
    )

    submit = SubmitField(_("UPDATE_SEMESTER_LABEL"))
