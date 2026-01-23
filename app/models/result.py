from operator import call
from typing import Dict

from app.extensions import db


class Result(db.Model):
    __tablename__ = "results"

    obtained_marks = db.Column(db.Integer, nullable=False)

    exam_id = db.Column(db.String(8), db.ForeignKey("exams.uid"), nullable=False)

    student_id = db.Column(db.String(8), db.ForeignKey("students.uid"), nullable=False)

    student = db.relationship("Student", back_populates="results")
    exam = db.relationship("Exam", back_populates="results")

    def to_dict(self) -> Dict:
        return {
            "obtained_marks": self.obtained_marks,
            "exam_id": self.exam_id,
            "student_id": self.student_id,
            "student_name": self.student.full_name,
            "percentage": self.display_percentage,
            "status": self.status,
            **call(getattr(super(), "to_dict")),
        }

    @property
    def percentage(self):
        return round((self.obtained_marks / self.exam.total_marks) * 100, 2)

    @property
    def display_percentage(self):
        return f"{self.percentage}%"

    @property
    def status(self):
        return "Pass" if self.percentage >= self.exam.min_percentage else "Fail"
