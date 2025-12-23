from typing import Dict, Union

from numerize.numerize import numerize

from app.extensions import db
from app.models.employee import Employee
from app.models.teacher import Teacher


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
    def _head_of_department(self) -> Union[Employee, Teacher, None]:
        obj = None

        match self.head_of_department:
            case val if val.startswith("E"):
                obj = Employee.query.filter_by(uid=self.head_of_department).first()

            case val if val.startswith("T"):
                obj = Teacher.query.filter_by(uid=self.head_of_department).first()

        return obj

    @property
    def display_head_of_department_uid(self):
        return self.head_of_department if self.head_of_department else "N/A"

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
