from app.extensions import db


class Class(db.Model):
    __tablename__ = "classes"

    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"))
    semester_id = db.Column(db.String(8), db.ForeignKey("semesters.uid"))

    teacher = db.relationship("Teacher", back_populates="classes")
    students = db.relationship("Student", back_populates="class_")
    semester = db.relationship("Semester", back_populates="classes")

    def __repr__(self):
        return f"<Class {self.name} Teacher={self.teacher_id}>"

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            **super().to_dict(),
        }
