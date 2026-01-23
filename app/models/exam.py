from operator import call
from typing import Dict

from numerize.numerize import numerize

from app.extensions import db
from app.models.result import Result


class Exam(db.Model):
    __tablename__ = "exams"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    exam_date = db.Column(db.Date, nullable=False)
    exam_time = db.Column(db.Time, nullable=False)

    total_marks = db.Column(db.Integer, nullable=False, default=100)
    min_marks = db.Column(db.Integer, nullable=False, default=50)

    subject_id = db.Column(db.String(8), db.ForeignKey("subjects.uid"), nullable=False)
    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"), nullable=False)

    subject = db.relationship("Subject", back_populates="exams")
    class_ = db.relationship("Class", back_populates="exams")
    results = db.relationship(
        "Result",
        back_populates="exam",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    def to_dict(self) -> Dict:
        return {
            "class_id": self.class_id,
            "subject_id": self.subject_id,
            "title": self.title,
            "description": self.description,
            "exam_date": self.display_exam_date,
            "exam_time": self.display_exam_time,
            "total_marks": self.total_marks,
            "min_marks": self.min_marks,
            "subject": self.subject.name,
            "class": self.class_.name,
            **call(getattr(super(), "to_dict")),
        }

    @property
    def passed(self):
        return Result.query.filter(Result.obtained_marks > self.min_marks)

    @property
    def failed(self):
        return Result.query.filter(Result.obtained_marks < self.min_marks)

    @property
    def get_passed(self):
        return self.passed.all()

    @property
    def get_failed(self):
        return self.failed.all()

    @property
    def min_percentage(self):
        return round((self.min_marks / self.total_marks) * 100, 2)

    @property
    def display_exam_date(self):
        return self.exam_date.strftime("%Y-%m-%d")

    @property
    def display_exam_time(self):
        return self.exam_time.strftime("%H:%M")

    @property
    def display_number_of_results(self):
        return numerize(self.results.count())

    @property
    def display_number_of_passed(self):
        return numerize(self.passed.count())

    @property
    def display_number_of_failed(self):
        return numerize(self.failed.count())
