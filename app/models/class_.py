from app.extensions import db


class Class(db.Model):
    __tablename__ = "classes"

    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    semester_id = db.Column(
        db.String(8), db.ForeignKey("semesters.uid"), nullable=False
    )

    teacher = db.relationship("Teacher", back_populates="classes")
    students = db.relationship("Student", back_populates="class_")
    semester = db.relationship("Semester", back_populates="classes")
    exams = db.relationship(
        "Exam", back_populates="class_", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Class {self.name} Teacher={self.teacher_id}>"

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "semester_id": self.semester_id,
            **super().to_dict(),
        }
