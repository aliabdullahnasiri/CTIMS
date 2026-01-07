from datetime import date, datetime, timezone
from typing import Dict, List, Union

import humanize
from flask import url_for
from numerize.numerize import numerize

from app.constants import DEFAULT_AVATAR
from app.extensions import db
from app.functions import get_file_url
from app.models.file import StudentFile
from app.models.phone import StudentPhone


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

    attendances = db.relationship(
        "StudentAttendance",
        back_populates="student",
        cascade="all, delete, delete-orphan",
    )
    class_ = db.relationship("Class", back_populates="students")
    phones = db.relationship(
        "StudentPhone", back_populates="student", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "StudentFile", back_populates="student", cascade="all, delete, delete-orphan"
    )
    results = db.relationship(
        "Result", back_populates="student", cascade="all, delete, delete-orphan"
    )

    @property
    def total_file_size(self) -> str:
        total: int = 0
        for f in self.files:
            total += f.file.size
        return humanize.naturalsize(total)

    @property
    def display_number_of_files(self):
        return numerize(len(self.files), decimals=2)

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

    @property
    def display_number_of_phone_nums(self):
        return numerize(len(self.phones), decimals=2)

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "class_id": self.class_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
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

    def update_phones(self, phones: List[str]):
        for phone in self.phones:
            if phone.phone_number not in phones:
                db.session.delete(phone)

        db.session.commit()

        for p in phones:
            if StudentPhone.query.filter_by(
                student_id=self.uid, phone_number=p
            ).first():
                continue

            phone = StudentPhone()
            phone.student_id = self.uid
            phone.phone_number = p

            db.session.add(phone)

        db.session.commit()

    def update_files(self, files: Dict[str, Union[str, List[str]]]) -> None:
        for key, value in files.items():
            match key:
                case "avatar" if type(value) == str:
                    self.avatar_path = get_file_url(value)
                    db.session.commit()
                case "files" if type(value) == list:
                    for file in self.files:
                        if file.file.uid not in value:
                            db.session.delete(file)
                            db.session.delete(file.file)

                    db.session.commit()

                    for val in value:
                        if StudentFile.query.filter_by(
                            student_id=self.uid, file_id=val
                        ).first():
                            continue

                        sf: StudentFile = StudentFile()
                        sf.student_id = self.uid
                        sf.file_id = val

                        db.session.add(sf)

                    db.session.commit()
