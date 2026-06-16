from flask_babel import gettext as _
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form, MustBeUnique, ValidateUID
from app.models.daily_section import DailySection
from app.models.exam import Exam


class AddDailySectionForm(Form):
    exam_uid = StringField(
        _("EXAM_UID_LABEL"),
        validators=[
            Optional(),
            ValidateUID(Exam),
            MustBeUnique(Exam, "uid"),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Exam",
            "data-select-val": "uid",
            "data-search-col": "title",
            "data-template": "exams.html",
        },
    )

    title = StringField(
        _("TITLE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255, message=_("THIS_FIELD_CANNOT_EXCEED_255_CHARACTERS_MSG")),
        ],
    )

    description = TextAreaField(
        _("DESCRIPTION_LABEL"),
    )

    submit = SubmitField(_("ADD_LABEL"))


class UpdateDailySectionForm(AddDailySectionForm):
    uid = HiddenField(
        _("DAILY_SECTION_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(DailySection),
        ],
    )

    submit = SubmitField(_("UPDATE_LABEL"))
