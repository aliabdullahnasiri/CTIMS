from typing import Dict

from numerize.numerize import numerize

from app.extensions import console, db


class Subject(db.Model):
    __tablename__ = "subjects"

    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    credit = db.Column(db.Integer)

    department_id = db.Column(
        db.String(8), db.ForeignKey("departments.uid"), nullable=False
    )
    semester_id = db.Column(
        db.String(8), db.ForeignKey("semesters.uid"), nullable=False
    )

    department = db.relationship("Department", back_populates="subjects")
    semester = db.relationship("Semester", back_populates="subjects")
    teachings = db.relationship(
        "Teaching", back_populates="subject", cascade="all, delete-orphan"
    )
    files = db.relationship(
        "SubjectFile", back_populates="subject", cascade="all, delete, delete-orphan"
    )
    exams = db.relationship(
        "Exam", back_populates="subject", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "credit": self.credit if self.credit else None,
            "department_uid": self.department_id,
            "semester_uid": self.semester_id,
            "teachers": [t.teacher_id for t in self.teachings],
            "files": [f.file.to_dict() for f in self.files],
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Subject {self.name}>"

    @property
    def display_number_of_teachers(self):
        return numerize(len({t.teacher.uid for t in self.teachings}))
