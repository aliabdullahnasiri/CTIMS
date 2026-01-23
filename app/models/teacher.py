from operator import call
from typing import List

from app.constants import CURRENCY_SYMBOL
from app.extensions import db
from app.models.subject import Subject


class Teacher(db.Model):
    __tablename__ = "teachers"

    time_id = db.Column(db.String(8), db.ForeignKey("times.uid"), nullable=False)
    user_uid = db.Column(
        db.String(8), db.ForeignKey("users.uid"), nullable=False, unique=True
    )
    salary = db.Column(db.Numeric(12, 2), nullable=True)

    time = db.relationship("Time", back_populates="teachers")
    user = db.relationship("User", cascade="delete")

    attendances = db.relationship(
        "TeacherAttendance",
        back_populates="teacher",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    classes = db.relationship(
        "Class",
        back_populates="teacher",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    @property
    def display_salary(self) -> str:
        return (
            f"{CURRENCY_SYMBOL}{float(self.salary):,.2f}"
            if self.salary is not None
            else "N/A"
        )

    @property
    def is_salary_gt_avg(self) -> bool:
        teachers = self.query.all()
        salaries = [float(t.salary) for t in teachers if t.salary is not None]
        if not salaries or self.salary is None:
            return False
        avg_salary = sum(salaries) / len(salaries)
        return float(self.salary) > avg_salary

    def to_dict(self):
        dct = {
            "teacher_id": getattr(self, "uid"),
            "user_uid": self.user.uid,
            "time_id": self.time_id,
            "full_name": self.user.full_name,
            "first_name": self.user.first_name,
            "middle_name": self.user.middle_name,
            "last_name": self.user.last_name,
            "user_name": self.user.user_name,
            "email": self.user.email,
            "birthday": self.user.display_birthday,
            "age": self.user.age,
            "salary": f"{self.salary:.2f}" if self.salary is not None else None,
            "display_salary": self.display_salary,
            "avatar": self.user.avatar_path,
            "files": [f.to_dict() for f in self.user.files.all()],
            "phones": [p.number for p in self.user.phones.all()],
            "subjects": [s.uid for s in getattr(self, "subjects").all()],
            **call(getattr(super(), "to_dict")),
        }

        return dct

    def update_subjects(self, subjects: List[str]):
        __subjects__ = getattr(self, "subjects")

        print(list(__subjects__.all()))
        for subject in __subjects__.all():
            if subject.uid not in subjects:
                __subjects__.remove(subject)

        for subject in subjects:
            if __subjects__.filter_by(uid=subject).scalar():
                continue

            subject = Subject.query.filter_by(uid=subject).scalar()
            __subjects__.append(subject)

    def __repr__(self):
        return f"<Teacher full_name={self.user.full_name!r}>"
