import json
import re
from operator import and_
from typing import List, Self

from flask import url_for
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import ValidationError

from app.const import UID_PATTERN


class MustBeUnique:
    def __init__(
        self: Self, model, name, message=None, col="uid", field="uid", format=False
    ) -> None:
        self.model = model
        self.name = name
        self.col = col
        self.field = field
        self.message = message
        self.format = format

    def __call__(self, form, field):
        vals: List = []

        try:
            vals = json.loads(field.data)
        except:
            vals.append(field.data)

        for val in vals:
            if (
                self.model.query.filter(
                    and_(
                        (
                            getattr(self.model, self.col)
                            != getattr(
                                getattr(form, _f),
                                "data",
                            )
                        ),
                        getattr(self.model, self.name) == val,
                    )
                ).count()
                if "Update" in form.__class__.__name__
                and hasattr(
                    form,
                    (
                        _f := (
                            self.field
                            if self.model.__name__ in form.__class__.__name__
                            or self.format
                            else f"{self.model.__name__.lower()}_{self.field}"
                        )
                    ),
                )
                else self.model.query.filter(
                    getattr(self.model, self.name) == val,
                ).count()
            ):
                raise ValidationError(_(self.message))


class ValidateUID:
    def __init__(
        self: Self,
        model,
        invalid_format_msg=None,
        not_found_msg=None,
    ) -> None:
        self.model = model
        self.prefix = model.__class__.__name__.__getitem__(0)
        self.invalid_format_msg = invalid_format_msg
        self.not_found_msg = not_found_msg

    def __call__(self, form, field):
        pattern: re.Pattern = re.compile(UID_PATTERN)

        vals: List = []

        try:
            vals = json.loads(field.data)
        except:
            vals.append(field.data)

        for val in vals:
            if not pattern.search(val):
                raise ValidationError(_(self.invalid_format_msg or "NOT_VALID_UID_MSG"))

            if not self.model.query.filter_by(uid=val).count():
                raise ValidationError(
                    _(self.not_found_msg or "SPECIFIED_RECORD_DOES_NOT_EXIST")
                )


class Form(FlaskForm):
    def __new__(cls, *args, **kwargs) -> Self:
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Translate all field labels so individual form files don't need to call _ for each label
        for _field in getattr(self, "_fields", {}).values():
            try:
                if _field.render_kw and (
                    endpoint := _field.render_kw.get("data-fetch-api")
                ):
                    _field.render_kw["data-fetch-api"] = url_for(endpoint)
            except:
                ...

            try:
                if isinstance(_field.label.text, str):
                    _field.label.text = _l(_field.label.text)
            except:
                ...

    def validate(self, *args, **kwargs):
        # Run the standard WTForms validation
        success = super().validate(*args, **kwargs)

        # If validation fails, intercept and translate the error messages
        if not success:
            for field in self:
                if field.errors:
                    # Pass each raw string error through gettext
                    field.errors = [_(error) for error in field.errors]

        return success
