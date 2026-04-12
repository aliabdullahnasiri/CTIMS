from operator import call
from typing import Dict, List

import humanize
from numerize.numerize import numerize
from sqlalchemy import func

from app.extensions.db import db
from app.models.file import File


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
    files = db.relationship(
        "File",
        secondary="subjects_files",
        backref=db.backref("subjects", lazy="dynamic"),
        lazy="dynamic",
    )

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
            "files": [f.to_dict() for f in self.files.all()],
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
        return numerize(self.files.count())

    @property
    def total_file_size(self) -> str:
        total: int = 0

        for f in self.files.all():
            total += f.size

        return humanize.naturalsize(total)

    def update_files(self, files: Dict[str, List[int]]) -> None:
        for key, vals in files.items():
            match key:
                case "files" if type(vals) == list:
                    for file in self.files.all():
                        if file.id not in vals:
                            db.session.delete(file)

                    for val in vals:
                        if file := File.query.filter_by(id=int(val)).scalar():
                            self.files.append(file)
