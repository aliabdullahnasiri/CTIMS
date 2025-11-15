from datetime import date, datetime, timezone

import humanize
from flask import url_for

from app.constants import DEFAULT_AVATAR
from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    birthday = db.Column(db.Date, nullable=True)

    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"))

    # Files
    avatar_path = db.Column(db.String(255), nullable=True)  # Path to avatar image

    attendances = db.relationship("StudentAttendance", back_populates="student")
    class_ = db.relationship("Class", back_populates="students")
    phones = db.relationship(
        "StudentPhone", back_populates="student", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "StudentFile", back_populates="student", cascade="all, delete, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)

    @property
    def age(self) -> int | None:
        if self.birthday is None:
            return None
        today = date.today()
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    @property
    def display_birthday(self) -> str:
        return self.birthday.strftime("%Y-%m-%d") if self.birthday else "N/A"

    @property
    def total_files_size(self) -> str:
        total = sum((f.file.size for f in self.files), start=0)
        return humanize.naturalsize(total)

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "class_id": self.class_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_path,
            "phones": [phone.phone_number for phone in self.phones],
            "files": [f.file.to_dict() for f in self.files],
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Student {self.full_name} ID={self.uid}>"
