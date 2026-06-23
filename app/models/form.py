from datetime import datetime
from enum import Enum
from operator import call

from app.extensions.db import db


class FormType(Enum):
    STUDENT_REGISTRATION_FORM = "StudentRegistrationForm"


class Form(db.Model):
    __tablename__ = "forms"

    distribution_date = db.Column(
        db.Date,
        nullable=False,
        default=lambda: datetime.now(),
    )

    name = db.Column(db.String(100), nullable=False)

    _type = db.Column(db.Enum(FormType), nullable=False)

    _path = db.Column(db.String(255))

    _hash = db.Column(db.String(255))

    students = db.relationship(
        "Student",
        secondary="student_form",
        backref=db.backref(
            "forms",
            lazy="dynamic",
        ),
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "distribution_date": call(
                getattr(self, "display_date"), "distribution_date"
            ),
            "type": self._type.value,
            "path": self._path,
            **call(getattr(super(), "to_dict")),
        }


class StudentForm(db.Model):
    __tablename__ = "student_form"

    __table_args__ = (
        db.UniqueConstraint(
            "student_uid",
            "form_uid",
            name="uc_student_form",
        ),
    )

    student_uid = db.Column(
        db.String(8),
        db.ForeignKey("students.uid"),
        nullable=False,
    )

    form_uid = db.Column(
        db.String(8),
        db.ForeignKey("forms.uid"),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"<StudentForm("
            f"student_uid='{self.student_uid}', "
            f"form_uid='{self.form_uid}')>"
        )

    def __str__(self):
        return f"{self.student_uid} -> {self.form_uid}"

    def to_dict(self):
        return {
            "student_uid": self.student_uid,
            "form_uid": self.form_uid,
            **call(getattr(super(), "to_dict")),
        }
