from typing import Dict, List, Union

import humanize
from numerize.numerize import numerize

from app.extensions import db
from app.models.file import File
from app.models.teaching import Teaching


class Subject(db.Model):
    __tablename__ = "subjects"

    name = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    credit = db.Column(db.Integer)

    semester_id = db.Column(
        db.String(8), db.ForeignKey("semesters.uid"), nullable=False
    )

    semester = db.relationship("Semester", back_populates="subjects")
    teachings = db.relationship(
        "Teaching", back_populates="subject", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "SubjectFile", back_populates="subject", cascade="all, delete, delete-orphan"
    )
    exams = db.relationship(
        "Exam", back_populates="subject", cascade="all, delete, delete-orphan"
    )

    @property
    def department(self):
        return self.semester.department

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "credit": self.credit if self.credit else None,
            "department_uid": self.department.uid,
            "semester_uid": self.semester_id,
            "teachers": [t.teacher_id for t in self.teachings],
            "files": [f.file.to_dict() for f in self.files],
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Subject {self.name}>"

    @property
    def teachers(self):
        return [t.teacher for t in self.teachings]

    @property
    def display_number_of_teachers(self):
        return numerize(len({t.teacher.uid for t in self.teachings}))

    @property
    def display_number_of_exams(self):
        return numerize(len(self.exams))

    @property
    def total_file_size(self) -> str:
        total: int = 0
        for f in self.files:
            total += f.file.size
        return humanize.naturalsize(total)

    @property
    def display_number_of_files(self):
        return numerize(len(self.files), decimals=2)

    def update_teachers(self, teachers: List[str]):
        for t in self.teachings:
            if t.teacher.uid not in teachers:
                db.session.delete(t)

        db.session.commit()

        for t in teachers:
            if Teaching.query.filter_by(subject_id=self.uid, teacher_id=t).first():
                continue

            teaching = Teaching()
            teaching.subject_id = self.uid
            teaching.teacher_id = t

            db.session.add(teaching)

        db.session.commit()

    def update_files(self, files: Dict[str, Union[str, List[str]]]) -> None:
        for key, value in files.items():
            match key:
                case "files" if type(value) == list:
                    for file in self.files:
                        if file.uid not in value:
                            db.session.delete(file)

                    db.session.commit()

                    for val in value:
                        if file := File.query.filter_by(file_id=val).first():
                            file.file_for = self.uid

                    db.session.commit()
