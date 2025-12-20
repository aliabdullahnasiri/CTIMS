from numerize.numerize import numerize

from app.extensions import db


class Class(db.Model):
    __tablename__ = "classes"

    name = db.Column(db.String(100), nullable=False, unique=True)
    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    semester_id = db.Column(
        db.String(8), db.ForeignKey("semesters.uid"), nullable=False
    )
    time_id = db.Column(db.String(8), db.ForeignKey("times.uid"), nullable=False)

    time = db.relationship("Time", back_populates="classes")
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
            "time_id": self.time_id,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "semester_id": self.semester_id,
            **super().to_dict(),
        }

    @property
    def number_of_students(self) -> int:
        return len(self.students)

    @property
    def display_number_of_students(self) -> str:
        return numerize(self.number_of_students, decimals=2)
