from operator import call
from typing import Dict

from app.extensions.db import db


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

    def to_dict(self) -> Dict:
        return {
            "exam_uid": self.exam_uid,
            "title": self.title,
            "description": self.description,
            "students": [student.to_dict() for student in self.students.all()],
            **call(getattr(super(), "to_dict")),
        }
