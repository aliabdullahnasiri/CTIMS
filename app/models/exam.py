from typing import Dict

from app.extensions import db


class Exam(db.Model):
    __tablename__ = "exams"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    exam_date = db.Column(db.Date, nullable=False)
    exam_time = db.Column(db.Time, nullable=False)

    total_marks = db.Column(db.Integer, nullable=False, default=100)

    subject_id = db.Column(db.String(8), db.ForeignKey("subjects.uid"), nullable=False)
    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"), nullable=False)

    subject = db.relationship("Subject", back_populates="exams")
    class_ = db.relationship("Class", back_populates="exams")
    results = db.relationship(
        "Result", back_populates="exam", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "uid": self.uid,
            "class_id": self.class_id,
            "subject_id": self.subject_id,
            "title": self.title,
            "description": self.description,
            "exam_date": self.display_exam_date,
            "exam_time": self.display_exam_time,
            "total_marks": self.total_marks,
            "subject": self.subject.name,
            "class": self.class_.name,
        }

    @property
    def display_exam_date(self):
        return self.exam_date.strftime("%Y-%m-%d")

    @property
    def display_exam_time(self):
        return self.exam_time.strftime("%H:%M")
