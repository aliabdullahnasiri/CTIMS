from operator import call
from typing import Dict

from sqlalchemy import and_

from app.extensions.db import db
from app.models.exam import Exam
from app.models.result import Result


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
    def passed_students(self):
        return (
            result.student
            for result in Result.query.join(
                Exam, Result.exam_id == getattr(Exam, "uid")
            )
            .filter(
                and_(
                    Result.exam_id == self.exam_uid,
                    (Result.obtained_marks * 100.0 / Exam.total_marks)
                    >= Exam.min_percentage,
                )
            )
            .all()
        )

    @property
    def get_next_base_number(self):
        Student = db.Model.registry._class_registry.get("Student")

        student = (
            Student.query.filter(Student.base_number > 0)
            .order_by(Student.base_number.desc())
            .first()
        )

        if student:
            return student.base_number + 1

        return self.starting_base_number

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
