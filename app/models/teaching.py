from operator import call

from sqlalchemy import UniqueConstraint

from app.extensions.db import db


class Teaching(db.Model):
    __tablename__ = "teachings"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    subject_id = db.Column(db.String(8), db.ForeignKey("subjects.uid"), nullable=False)

    __table_args__ = (
        UniqueConstraint("teacher_id", "subject_id", name="uix_teacher_subject"),
    )

    def to_dict(self) -> dict:
        return {
            "teacher_id": self.teacher_id,
            "subject_id": self.subject_id,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Teach Teacher={self.teacher_id} Subject={self.subject_id}>"
