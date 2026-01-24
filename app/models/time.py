from operator import call
from typing import Dict

from numerize.numerize import numerize

from app.extensions import db


class Time(db.Model):
    __tablename__ = "times"

    title = db.Column(db.String(50))
    description = db.Column(db.String(255))

    start = db.Column(db.Time, nullable=True)
    end = db.Column(db.Time, nullable=True)

    classes = db.relationship(
        "Class",
        back_populates="time",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    teachers = db.relationship(
        "Teacher",
        back_populates="time",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "start": self.display_start_time,
            "end": self.display_end_time,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Time {self.title}>"

    @property
    def display_start_time(self) -> str:
        return self.start.strftime("%H:%M") if self.start else "N/A"

    @property
    def display_end_time(self) -> str:
        return self.end.strftime("%H:%M") if self.end else "N/A"

    @property
    def display_number_of_classes(self) -> str:
        return numerize(self.classes.count(), decimals=2)

    @property
    def display_number_of_students(self) -> str:
        n = 0

        for class_ in self.classes.all():
            n += class_.number_of_students

        return numerize(n, decimals=2)

    @property
    def display_number_of_teachers(self) -> str:
        return numerize(self.teachers.count())

    @property
    def students(self):
        students = None

        for cls in self.classes.all():
            if students is None:
                students = cls.students
            else:
                students.union(cls.students)

        return students
