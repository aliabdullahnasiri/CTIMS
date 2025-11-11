from app.extensions import db


class Class(db.Model):
    __tablename__ = "classes"

    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"))

    teacher = db.relationship("Teacher", back_populates="classes")
    students = db.relationship("Student", back_populates="class_")

    def __repr__(self):
        return f"<Class {self.name} Teacher={self.teacher_id}>"

    def to_dict(self):
        return {
            "class_id": self.uid,
            "class_name": self.name,
            "teacher": self.teacher.to_dict(),
            "students": [student.to_dict() for student in self.students],
            **super().to_dict(),
        }
