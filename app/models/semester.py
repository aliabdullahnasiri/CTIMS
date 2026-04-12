from operator import call

from numerize.numerize import numerize

from app.extensions.db import db


class Semester(db.Model):
    __tablename__ = "semesters"

    name = db.Column(db.String(50))
    number = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.String(8), db.ForeignKey("departments.uid"), nullable=False
    )

    department = db.relationship("Department", back_populates="semesters")
    subjects = db.relationship(
        "Subject",
        back_populates="semester",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    classes = db.relationship(
        "Class",
        back_populates="semester",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    students = db.relationship(
        "Student",
        secondary="classes",
        lazy="dynamic",
        viewonly=True,
    )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "number": self.number,
            "department_uid": self.department_id,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Semester name={self.name!r}>"

    @property
    def display_number_of_classes(self):
        return numerize(self.classes.count(), decimals=2)

    @property
    def display_number_of_subjects(self):
        return numerize(len(self.get_all_subjects()), decimals=2)

    @property
    def display_number_of_students(self):
        return numerize(
            len([y for x in self.classes.all() for y in x.students]), decimals=2
        )

    @property
    def display_number_of_teachers(self):
        return numerize(
            sum({subject.teachers.count() for subject in self.get_all_subjects()})
        )

    @property
    def display_number_of_exams(self):
        return numerize(
            len([e for s in self.get_all_subjects() for e in s.exams]), decimals=2
        )

    @property
    def teachers(self):
        return [
            teach.teacher
            for subject in self.get_all_subjects()
            for teach in subject.teachings
        ]

    @property
    def exams(self):
        return [exam for subject in self.get_all_subjects() for exam in subject.exams]

    @property
    def results(self):
        return [
            result
            for subject in self.get_all_subjects()
            for exam in subject.exams
            for result in exam.results
        ]

    def get_all_subjects(self):
        subjects = {subject for subject in self.subjects.all()}

        for department in self.department.get_parent_departments():
            for subject in department.subjects:
                if subject.semester.number == self.number:
                    subjects.add(subject)

        return subjects
