from operator import call
from typing import Dict, Union

from numerize.numerize import numerize
from sqlalchemy import and_

from app.extensions.db import db
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
        "Semester",
        back_populates="department",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    departments = db.relationship(
        "Department",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    subjects = db.relationship(
        "Subject",
        secondary="semesters",
        backref="subjects",
        lazy="dynamic",
        viewonly=True,
    )
    classes = db.relationship(
        "Class",
        secondary="semesters",
        lazy="dynamic",
        viewonly=True,
    )

    @property
    def teachers(self):
        return {
            teacher
            for subject in self.subjects.all()
            for teacher in subject.teachers.all()
        }

    @property
    def students(self):
        return {student for cls in self.classes.all() for student in cls.students.all()}

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "head_of_department": self.head_of_department,
            "parent_department_uid": self.parent_department_uid,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Department name={self.name!r}>"

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
    def head_of_department_entity_label(self) -> Union[str, None]:
        if self.head_of_department:
            match self.head_of_department:
                case val if val.startswith("E"):
                    return "Employee"

                case val if val.startswith("T"):
                    return "Teacher"

    @property
    def _head_of_department_uid(self):
        return self.head_of_department

    @property
    def display_head_of_department_uid(self):
        return self.head_of_department if self.head_of_department else "N/A"

    @property
    def display_parent_department_uid(self):
        return self.parent_department_uid if self.parent_department_uid else "N/A"

    @property
    def display_number_of_semesters(self):
        return numerize(self.semesters.count())

    @property
    def display_number_of_all_semesters(self):
        return numerize(len(self.get_all_semesters()))

    @property
    def display_number_of_all_classes(self):
        return numerize(
            sum(semester.classes.count() for semester in self.get_all_semesters())
        )

    @property
    def display_number_of_all_students(self):
        return numerize(
            sum(semester.classes.count() for semester in self.get_all_semesters())
        )

    @property
    def display_number_of_all_teachers(self):
        return numerize(
            len(
                {
                    teacher
                    for semester in self.get_all_semesters()
                    for subject in semester.subjects.all()
                    for teacher in subject.teachers
                }
            )
        )

    @property
    def display_number_of_classes(self):
        return numerize(self.classes.count())

    @property
    def display_number_of_students(self):
        count = 0

        for cls in self.classes.all():
            count += cls.students.count()

        return count

    @property
    def display_number_of_teachers(self):
        return numerize(
            len(
                {
                    teacher
                    for subject in self.subjects.all()
                    for teacher in subject.teachers.all()
                }
            )
        )

    @property
    def display_number_of_subjects(self):
        return numerize(self.subjects.count())

    @property
    def display_number_of_all_subjects(self):
        count = self.subjects.count()

        for department in self.get_parent_departments():
            count += department.subjects.count()

        return count

    def get_parent_department(self):
        if self.parent_department_uid:
            return (
                db.session.query(Department)
                .filter_by(uid=self.parent_department_uid)
                .first()
            )

    def get_parent_departments(self, department=None) -> list:
        if getattr(self, "uid") == self.parent_department_uid:
            return []

        return list(
            filter(
                lambda item: item is not None,
                [
                    (
                        parent := db.session.query(Department)
                        .filter(
                            and_(
                                (
                                    (getattr(Department, "uid") != department.uid)
                                    if department
                                    else True
                                ),
                                getattr(Department, "uid")
                                == (
                                    self.parent_department_uid
                                    if not department
                                    else department.parent_department_uid
                                ),
                            )
                        )
                        .scalar()
                    )
                ]
                + (self.get_parent_departments(parent) if parent else []),
            )
        )

    def get_all_semesters(self):
        semesters = {semester.number: semester for semester in self.semesters.all()}

        for department in self.get_parent_departments():
            for semester in department.semesters.all():
                semesters.setdefault(semester.number, semester)

        return sorted(semesters.values(), key=lambda i: i.number, reverse=False)

    def get_all_subjects(self):
        subjects = {subject for subject in self.subjects.all()}

        for department in self.get_parent_departments():
            subjects |= set(department.subjects.all())

        return subjects

    def get_all_students(self):
        return {
            student
            for semester in self.get_all_semesters()
            for _class in semester.classes.all()
            for student in _class.students.all()
        }

    def get_all_teachers(self):
        return {
            teacher
            for semester in self.get_all_semesters()
            for subject in semester.subjects.all()
            for teacher in subject.teachers
        }

    def get_all_classes(self):
        return {
            _class
            for semester in self.get_all_semesters()
            for _class in semester.classes.all()
        }
