from operator import call
from typing import Dict

from sqlalchemy import case
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions.db import db


class Result(db.Model):
    __tablename__ = "results"

    obtained_marks = db.Column(db.Integer, nullable=False)

    exam_id = db.Column(db.String(8), db.ForeignKey("exams.uid"), nullable=False)

    student_id = db.Column(db.String(8), db.ForeignKey("students.uid"), nullable=False)

    student = db.relationship("Student", back_populates="results", lazy="select")
    exam = db.relationship("Exam", back_populates="results")

    def to_dict(self) -> Dict:
        return {
            "obtained_marks": self.obtained_marks,
            "exam_id": self.exam_id,
            "student_id": self.student_id,
            "student_name": self.student.user.full_name,
            "percentage": self.display_percentage,
            "status": self.status,
            **call(getattr(super(), "to_dict")),
        }

    @hybrid_property
    def passed(self):
        return (
            self.obtained_marks * 100.0 / self.exam.total_marks
        ) >= self.exam.min_percentage

    @passed.expression
    def passed(cls):
        Exam = getattr(db.Model, "registry")._class_registry.get("Exam")

        return case(
            (
                (Result.obtained_marks * 100.0 / Exam.total_marks)
                >= Exam.min_percentage,
                True,
            ),
            else_=False,
        )

    @property
    def percentage(self):
        return round((self.obtained_marks * 100.0 / self.exam.total_marks), 2)

    @property
    def display_percentage(self):
        return f"{self.percentage}%"

    @property
    def status(self):
        return "Pass" if self.passed else "Fail"

    @property
    def is_passed(self):
        return self.passed
