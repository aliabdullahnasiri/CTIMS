from app.extensions import db


class Teaching(db.Model):
    __tablename__ = "teachings"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    subject_id = db.Column(db.String(8), db.ForeignKey("subjects.uid"), nullable=False)

    teacher = db.relationship("Teacher", back_populates="teachings")
    subject = db.relationship("Subject", back_populates="teachings")

    def to_dict(self) -> dict:
        return {
            "teacher_id": self.teacher_id,
            "subject_id": self.subject_id,
            "teacher": self.teacher.to_dict(),
            "subject": self.subject.to_dict(),
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Teach Teacher={self.teacher_id} Subject={self.subject_id}>"
