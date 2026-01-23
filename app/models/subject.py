from operator import call
from typing import Dict, List, Union

import humanize
from numerize.numerize import numerize

from app.extensions import db
from app.models.file import File
from app.models.teaching import Teaching
from app.models.user import User


class Subject(db.Model):
    __tablename__ = "subjects"

    name = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    credit = db.Column(db.Integer)
    semester_id = db.Column(
        db.String(8), db.ForeignKey("semesters.uid"), nullable=False
    )

    semester = db.relationship("Semester", back_populates="subjects")
    teachers = db.relationship(
        "Teacher",
        secondary="teachings",
        backref=db.backref("subjects", lazy="dynamic"),
        lazy="dynamic",
    )
    exams = db.relationship(
        "Exam",
        back_populates="subject",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    @property
    def files(self):
        return [
            file for file in File.query.filter_by(file_for=getattr(self, "uid")).all()
        ]

    @property
    def department(self):
        return self.semester.department

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "credit": self.credit,
            "department_uid": self.department.uid,
            "semester_uid": self.semester_id,
            "teachers": [t.uid for t in self.teachers.all()],
            "files": [f.to_dict() for f in self.files],
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Subject name={self.name!r}>"

    @property
    def display_number_of_teachers(self):
        return numerize(self.teachers.count())

    @property
    def display_number_of_exams(self):
        return numerize(self.exams.count())

    @property
    def display_number_of_files(self):
        return numerize(len(self.files), decimals=2)

    @property
    def total_file_size(self) -> str:
        total: int = 0

        for f in self.files:
            total += f.size

        return humanize.naturalsize(total)

    def update_teachers(self, teachers: List[str]):
        for t in self.teachers.all():
            if t.uid not in teachers:
                self.teachers.remove(t)

        for t in teachers:
            if self.teachers.filter_by(uid=t).scalar():
                continue

            teaching = Teaching()
            teaching.teacher_id = t

            self.teachers.add(teaching)

    def update_files(self, files: Dict[str, Union[int, List[int]]]) -> None:
        return call(getattr(User, "update_files"), self, files)
