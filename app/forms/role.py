import json
import re

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional, ReadOnly

from app.models.permission import Permission


class UpdateRoleForm(FlaskForm):
    uid = HiddenField("Role UID", validators=[DataRequired()])
    name = StringField("Name", validators=[ReadOnly(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField("Default", default=False, validators=[Optional()])
    permissions = StringField("Permissions", validators=[Optional()])

    submit = SubmitField("Update Role")

    def validate_permissions(self, permissions):
        permissions = json.loads(permissions.data)
        pattern: re.Pattern = re.compile(r"^P.\d{6}$")

        if any(filter(lambda permission: not pattern.search(permission), permissions)):
            raise ValidationError("Not a valid Permission UID.")

        for permission in permissions:
            if not Permission.query.filter_by(uid=permission).first():
                raise ValidationError("Permission with the given ID was not found :(")
