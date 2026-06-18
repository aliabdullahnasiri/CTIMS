from flask_babel import gettext as _
from wtforms import (
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import ValidateUID
from app.forms.user import AddUserForm, UpdateUserForm
from app.models.class_ import Class
from app.models.student import IdentityCardType, Student
from app.models.user import User


class AddStudentForm(AddUserForm):
    father_name = StringField(
        _("FATHER_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255),
        ],
    )

    grandfather_name = StringField(
        _("GRANDFATHER_NAME_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            Length(max=255),
        ],
    )

    kankor_id = StringField(
        _("KANKOR_ID"),
        validators=[
            Optional(),
            Length(max=12),
        ],
    )

    identity_card_type = SelectField(
        _("IDENTITY_CARD_TYPE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
        ],
        choices=[
            (IdentityCardType.ELECTRONIC, _("ELECTRONIC_TAZKIRA_LABEL")),
            (IdentityCardType.PAPER, _("PAPER_TAZKIRA_LABEL")),
        ],
        render_kw={"data-group-switcher": "true"},
    )

    electronic_tazkira_number = StringField(
        _("ELECTRONIC_TAZKIRA_NUMBER_LABEL"),
        validators=[
            Optional(),
            Length(max=100),
        ],
        render_kw={"data-group-id": IdentityCardType.ELECTRONIC},
    )

    tazkira_folder = StringField(
        _("TAZKIRA_FOLDER_LABEL"),
        validators=[
            Optional(),
            Length(max=50),
        ],
        render_kw={"data-group-id": IdentityCardType.PAPER},
    )

    tazkira_page_number = StringField(
        _("TAZKIRA_PAGE_NUMBER_LABEL"),
        validators=[
            Optional(),
            Length(max=50),
        ],
        render_kw={"data-group-id": IdentityCardType.PAPER},
    )

    tazkira_registration_number = StringField(
        _("TAZKIRA_REGISTRATION_NUMBER_LABEL"),
        validators=[
            Optional(),
            Length(max=50),
        ],
        render_kw={"data-group-id": IdentityCardType.PAPER},
    )

    tazkira_sakok_number = StringField(
        _("TAZKIRA_SAKOK_NUMBER_LABEL"),
        validators=[
            Optional(),
            Length(max=50),
        ],
        render_kw={"data-group-id": IdentityCardType.PAPER},
    )

    # Permanent Address
    permanent_province = SelectField(
        _("PERMANENT_PROVINCE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
        ],
        choices=[],
    )

    permanent_district = SelectField(
        _("PERMANENT_DISTRICT_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
        ],
        choices=[],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "District",
            "data-option-value": "uid",
            "data-option-text": "name",
            "data-depends-on": "permanent_province",
        },
    )

    permanent_village = StringField(
        _("PERMANENT_VILLAGE_LABEL"),
        validators=[Optional(), Length(max=255)],
    )

    # Current Address
    current_province = SelectField(
        _("CURRENT_PROVINCE_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
        ],
        choices=[],
    )

    current_district = SelectField(
        _("CURRENT_DISTRICT_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
        ],
        choices=[],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "District",
            "data-option-value": "uid",
            "data-option-text": "name",
            "data-depends-on": "current_province",
        },
    )

    current_village = StringField(
        _("CURRENT_VILLAGE_LABEL"),
        validators=[Optional(), Length(max=255)],
    )

    submit = SubmitField(_("ADD_LABEL"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Translate all field labels so individual form files don't need to call _ for each label
        for _field in getattr(self, "_fields", {}).values():
            try:
                if (
                    isinstance(_field, (SelectField, SelectMultipleField))
                    and "province" in _field.name
                ):
                    ...
            except:
                pass

    def validate(self, extra_validators=None) -> bool:
        super().validate(extra_validators)

        tz_type = self.identity_card_type.data

        # ELECTRONIC tazkira rules
        if tz_type == IdentityCardType.ELECTRONIC:
            if not self.electronic_tazkira_number.data:
                self.electronic_tazkira_number.errors.append(
                    _("THIS_FIELD_IS_REQUIRED_ERROR")
                )
                return False

        # PAPER tazkira rules
        elif tz_type == IdentityCardType.PAPER:
            paper_fields = [
                self.tazkira_folder.data,
                self.tazkira_page_number.data,
                self.tazkira_registration_number.data,
                self.tazkira_sakok_number.data,
            ]

            if not any(paper_fields):
                msg = _("THIS_FIELD_IS_REQUIRED_ERROR")

                self.tazkira_folder.errors.append(msg)
                self.tazkira_page_number.errors.append(msg)
                self.tazkira_registration_number.errors.append(msg)
                self.tazkira_sakok_number.errors.append(msg)

                return False

        return True


class UpdateStudentForm(UpdateUserForm, AddStudentForm):
    uid = HiddenField(
        _("STUDENT_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(Student),
        ],
    )
    user_uid = HiddenField(
        _("USER_UID_LABEL"),
        validators=[
            DataRequired(message=_("THIS_FIELD_IS_REQUIRED_ERROR")),
            ValidateUID(User),
        ],
    )
    class_id = StringField(
        _("CLASS_UID_LABEL"),
        validators=[
            Optional(),
            Length(8, 8, message=_("THIS_FIELD_MUST_BE_8_CHARACTERS_MSG")),
            ValidateUID(Class),
        ],
        render_kw={
            "data-auto-complete": "true",
            "data-fetch-api": "api.autocomplete",
            "data-model-name": "Class",
            "data-select-val": "uid",
            "data-search-col": "name",
            "data-template": "classes.html",
        },
    )
    submit = SubmitField(_("UPDATE_STUDENT_LABEL"))
