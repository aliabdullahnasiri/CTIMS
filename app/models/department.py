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
    parent_department_uid = db.Column(
        db.String(8), db.ForeignKey("departments.uid"), nullable=True
    )

    semesters = db.relationship(
        "Semester", back_populates="department", cascade="all, delete, delete-orphan"
    )
    departments = db.relationship("Department")

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "head_of_department": self.head_of_department,
            "parent_department_uid": self.parent_department_uid,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Department {self.name}>"

    @property
    def subjects(self):
        return [subject for semester in self.semesters for subject in semester.subjects]

    @property
    def students(self):
        return [
            student
            for semester in self.semesters
            for _class in semester.classes
            for student in _class.students
        ]

    @property
    def teachers(self):
        return [
            teaching.teacher
            for semester in self.semesters
            for subject in semester.subjects
            for teaching in subject.teachings
        ]

    @property
    def classes(self):
        return [_class for semester in self.semesters for _class in semester.classes]

    @property
    def _head_of_department(self) -> Union[Employee, Teacher, None]:
        obj = None

        if self.head_of_department:
            match self.head_of_department:
                case val if val.startswith("E"):
                    obj = Employee.query.filter_by(uid=self.head_of_department).first()

                case val if val.startswith("T"):
                    obj = Teacher.query.filter_by(uid=self.head_of_department).first()

        return obj

    @property
    def _head_of_department_uid(self):
        return self.head_of_department

    @property
    def display_head_of_department_uid(self):
        return self.head_of_department if self.head_of_department else "N/A"

    @property
    def display_number_of_semesters(self):
        return numerize(len(self.semesters), decimals=2)

    @property
    def display_number_of_all_semesters(self):
        return numerize(len(self.get_all_semesters()), decimals=2)

    @property
    def display_number_of_classes(self):
        return numerize(len([c for s in self.semesters for c in s.classes]), decimals=2)

    @property
    def display_number_of_all_classes(self):
        return numerize(
            len([c for s in self.get_all_semesters() for c in s.classes]), decimals=2
        )

    @property
    def display_number_of_students(self):
        return numerize(len([y for x in self.semesters for y in x.classes]), decimals=2)

    @property
    def display_number_of_all_students(self):
        return numerize(
            len([y for x in self.get_all_semesters() for y in x.classes]), decimals=2
        )

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
    def display_number_of_all_teachers(self):
        return numerize(
            len(
                set(
                    [
                        z.teacher.uid
                        for y in self.get_all_semesters()
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

    @property
    def display_number_of_all_subjects(self):
        return numerize(len(self.get_all_subjects()), decimals=2)

    def get_parent_department(self):
        if self.parent_department_uid:
            return (
                db.session.query(Department)
                .filter_by(uid=self.parent_department_uid)
                .first()
            )

    def get_parent_departments(self, department=None) -> list:
        return list(
            filter(
                lambda item: item is not None,
                [
                    parent := db.session.query(Department)
                    .filter_by(
                        uid=(
                            self.parent_department_uid
                            if not department
                            else department.parent_department_uid
                        )
                    )
                    .first()
                ]
                + (self.get_parent_departments(parent) if parent else []),
            )
        )

    def get_all_semesters(self):
        semesters = {semester.number: semester for semester in self.semesters}

        for department in self.get_parent_departments():
            for semester in department.semesters:
                semesters.setdefault(semester.number, semester)

        return sorted(semesters.values(), key=lambda i: i.number, reverse=False)

    def get_all_subjects(self):
        subjects = [subject for subject in self.subjects]

        for department in self.get_parent_departments():
            subjects.extend(department.subjects)

        return subjects

    def get_all_students(self):
        return [
            student
            for semester in self.get_all_semesters()
            for _class in semester.classes
            for student in _class.students
        ]

    def get_all_teachers(self):
        return [
            teaching.teacher
            for semester in self.get_all_semesters()
            for subject in semester.subjects
            for teaching in subject.teachings
        ]

    def get_all_classes(self):
        return [
            _class
            for semester in self.get_all_semesters()
            for _class in semester.classes
        ]
