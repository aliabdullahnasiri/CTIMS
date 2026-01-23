from operator import call

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
    semester = db.relationship("Semester", back_populates="classes")
    students = db.relationship("Student", back_populates="class_", lazy="dynamic")
    exams = db.relationship(
        "Exam",
        back_populates="class_",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Class name={self.name!r}>"

    def to_dict(self):
        return {
            "time_id": self.time_id,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "semester_id": self.semester_id,
            **call(getattr(super(), "to_dict")),
        }

    @property
    def subjects(self):
        return self.semester.get_all_subjects()

    @property
    def attendances(self):
        return [
            attendance
            for student in self.students.all()
            for attendance in student.attendances.all()
        ]

    @property
    def results(self):
        return [result for exam in self.exams.all() for result in exam.results.all()]

    @property
    def number_of_subjects(self):
        return len(self.subjects)

    @property
    def number_of_exams(self):
        return self.exams.count()

    @property
    def number_of_students(self) -> str:
        return self.students.count()

    @property
    def display_number_of_students(self) -> str:
        return numerize(self.number_of_students)

    @property
    def display_number_of_all_subjects(self):
        return numerize(self.number_of_subjects)

    @property
    def display_number_of_exams(self):
        return numerize(self.number_of_exams)
