from typing import Dict

from numerize.numerize import numerize

from app.extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    name = db.Column(db.String(60))
    description = db.Column(db.String(255))
    head_of_department = db.Column(db.String(8))

    subjects = db.relationship(
        "Subject", back_populates="department", cascade="all, delete, delete-orphan"
    )
    semesters = db.relationship(
        "Semester", back_populates="department", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "head_of_department": self.head_of_department,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Department {self.name}>"

    @property
    def display_number_of_semesters(self):
        return numerize(len(self.semesters), decimals=2)

    @property
    def display_number_of_classes(self):
        return numerize(len([c for s in self.semesters for c in s.classes]), decimals=2)

    @property
    def display_number_of_students(self):
        return numerize(len([y for x in self.semesters for y in x.classes]), decimals=2)

    @property
    def display_number_of_teachers(self):
        return numerize(
            len(
                set(
                    [
                        z.teacher.uid
                        for y in self.semesters
                        for x in y.subjects
                        for z in x.teachings
                    ]
                )
            ),
            decimals=2,
        )

    @property
    def display_number_of_subjects(self):
        return numerize(
            len([y for x in self.semesters for y in x.subjects]), decimals=2
        )
