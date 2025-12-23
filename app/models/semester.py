from numerize.numerize import numerize

from app.extensions import db


class Semester(db.Model):
    __tablename__ = "semesters"

    name = db.Column(db.String(50))
    number = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.String(8), db.ForeignKey("departments.uid"), nullable=False
    )

    department = db.relationship("Department", back_populates="semesters")
    subjects = db.relationship(
        "Subject", back_populates="semester", cascade="all, delete, delete-orphan"
    )
    classes = db.relationship(
        "Class", back_populates="semester", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "number": self.number,
            "department_uid": self.department_id,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Semester {self.name} ID={self.uid}>"

    @property
    def display_number_of_classes(self):
        return numerize(len(self.classes), decimals=2)

    @property
    def display_number_of_subjects(self):
        return numerize(len(self.subjects), decimals=2)

    @property
    def display_number_of_students(self):
        return numerize(len([y for x in self.classes for y in x.students]), decimals=2)
