from operator import call
from typing import Dict

from sqlalchemy import and_, or_

from app.extensions.db import db
from app.models.exam import Exam
from app.models.result import Result
from app.models.student import Student


class DailySection(db.Model):
    __tablename__ = "daily_sections"

    exam_uid = db.Column(
        db.String(8),
        db.ForeignKey("exams.uid"),
        nullable=True,
        index=True,
        unique=True,
    )

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    starting_base_number = db.Column(db.Integer, nullable=False)
    academic_year = db.Column(db.SmallInteger, nullable=False)

    exam = db.relationship(
        "Exam",
        back_populates="daily_section",
    )

    students = db.relationship(
        "Student",
        back_populates="daily_section",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    @property
    def _students(self):
        return (
            self.students.outerjoin(
                Result,
                Result.student_id == getattr(Student, "uid"),
            )
            .filter(or_(Student.kankor_id.isnot(None), Result.passed.is_(True)))
            .order_by(Student.base_number.asc())
        )

    @property
    def get_next_base_number(self):
        Student = getattr(db.Model, "registry")._class_registry.get("Student")

        student = (
            Student.query.filter(Student.base_number > 0)
            .order_by(Student.base_number.desc())
            .first()
        )

        if student:
            return student.base_number + 1

        return self.starting_base_number

    @property
    def display_student_count(self):
        return self.students.count()

    def to_dict(self) -> Dict:
        return {
            "exam_uid": self.exam_uid,
            "title": self.title,
            "description": self.description,
            "starting_base_number": self.starting_base_number,
            "academic_year": self.academic_year,
            "students": [student.to_dict() for student in self.students.all()],
            **call(getattr(super(), "to_dict")),
        }
