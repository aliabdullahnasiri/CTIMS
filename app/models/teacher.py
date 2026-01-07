from datetime import date
from typing import Dict, List, Union

import humanize
from flask import url_for
from numerize.numerize import numerize

from app.constants import CURRENCY_SYMBOL, DEFAULT_AVATAR
from app.extensions import console, db
from app.functions import get_file, get_file_url
from app.models.file import TeacherFile
from app.models.phone import TeacherPhone
from app.models.teaching import Teaching


class Teacher(db.Model):
    __tablename__ = "teachers"

    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    birthday = db.Column(db.Date, nullable=True)

    avatar_path = db.Column(db.String(255), nullable=True)  # Path to avatar image
    salary = db.Column(db.Numeric(12, 2), nullable=True)

    time_id = db.Column(db.String(8), db.ForeignKey("times.uid"), nullable=False)

    time = db.relationship("Time", back_populates="teachers")

    teachings = db.relationship(
        "Teaching", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    attendances = db.relationship(
        "TeacherAttendance",
        back_populates="teacher",
        cascade="all, delete, delete-orphan",
    )
    classes = db.relationship(
        "Class", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    phones = db.relationship(
        "TeacherPhone", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "TeacherFile", back_populates="teacher", cascade="all, delete, delete-orphan"
    )

    @property
    def subjects(self):
        return [teaching.subject for teaching in self.teachings]

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
    def display_salary(self) -> str:
        return (
            f"{CURRENCY_SYMBOL}{float(self.salary):,.2f}"
            if self.salary is not None
            else "N/A"
        )

    @property
    def total_file_size(self) -> str:
        total: int = 0
        for f in self.files:
            total += f.file.size
        return humanize.naturalsize(total)

    @property
    def is_salary_gt_avg(self) -> bool:
        teachers = self.query.all()
        salaries = [float(t.salary) for t in teachers if t.salary is not None]
        if not salaries or self.salary is None:
            return False
        avg_salary = sum(salaries) / len(salaries)
        return float(self.salary) > avg_salary

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)

    @property
    def display_number_of_phone_nums(self):
        return numerize(len(self.phones), decimals=2)

    @property
    def display_number_of_classes(self):
        return numerize(len(self.classes), decimals=2)

    @property
    def display_number_of_files(self):
        return numerize(len(self.files), decimals=2)

    @property
    def display_number_of_teachings(self):
        return numerize(len(self.teachings), decimals=2)

    def to_dict(self):
        dct = {
            "teacher_id": self.uid,
            "time_id": self.time_id,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "salary": f"{self.salary:.2f}" if self.salary is not None else None,
            "display_salary": self.display_salary,
            "avatar": self.avatar_path,
            "phones": [p.phone_number for p in self.phones],
            "subjects": [s.subject.uid for s in self.teachings],
            "files": [f.file.to_dict() for f in self.files],
            **super().to_dict(),
        }

        return dct

    def update_subjects(self, subjects: List[str]):
        for teaching in self.teachings:
            if teaching.subject_id not in subjects:
                db.session.delete(teaching)

        db.session.commit()

        for subject in subjects:
            if Teaching.query.filter_by(
                subject_id=subject, teacher_id=self.uid
            ).first():
                continue

            teaching = Teaching()
            teaching.teacher_id = self.uid
            teaching.subject_id = subject

            db.session.add(teaching)

        db.session.commit()

    def update_phones(self, phones: List[str]):
        for phone in self.phones:
            if phone.phone_number not in phones:
                db.session.delete(phone)

        db.session.commit()

        for p in phones:
            if TeacherPhone.query.filter_by(
                teacher_id=self.uid, phone_number=p
            ).first():
                continue

            phone = TeacherPhone()
            phone.teacher_id = self.uid
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
                        if TeacherFile.query.filter_by(
                            teacher_id=self.uid, file_id=val
                        ).first():
                            continue

                        tf: TeacherFile = TeacherFile()
                        tf.file_id = val
                        tf.teacher_id = self.uid

                        db.session.add(tf)

                    db.session.commit()

    def __repr__(self):
        return f"<Teacher {self.full_name} ID={self.uid}>"
