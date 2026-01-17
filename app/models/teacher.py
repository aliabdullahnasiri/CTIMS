from typing import List

from numerize.numerize import numerize

from app.constants import CURRENCY_SYMBOL
from app.extensions import db
from app.models.file import File
from app.models.teaching import Teaching


class Teacher(db.Model):
    __tablename__ = "teachers"

    time_id = db.Column(db.String(8), db.ForeignKey("times.uid"), nullable=False)
    user_uid = db.Column(
        db.String(8), db.ForeignKey("users.uid"), nullable=False, unique=True
    )

    salary = db.Column(db.Numeric(12, 2), nullable=True)

    time = db.relationship("Time", back_populates="teachers")
    user = db.relationship("User")

    teachings = db.relationship(
        "Teaching", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    attendances = db.relationship(
        "TeacherAttendance",
        back_populates="teacher",
        cascade="all, delete, delete-orphan",
    )
    classes = db.relationship(
        "Class", back_populates="teacher", cascade="all, delete, delete-orphan"
    )

    @property
    def files(self):
        return [file for file in File.query.filter_by(file_for=self.user.uid).all()]

    @property
    def subjects(self):
        return [teaching.subject for teaching in self.teachings]

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

    @property
    def display_number_of_classes(self):
        return numerize(len(self.classes), decimals=2)

    @property
    def display_number_of_teachings(self):
        return numerize(len(self.teachings), decimals=2)

    def to_dict(self):
        dct = {
            "teacher_id": self.uid,
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
            "phones": [p.number for p in self.user.phones],
            "subjects": [s.subject.uid for s in self.teachings],
            "files": [f.to_dict() for f in self.files],
            **super().to_dict(),
        }

        return dct

    def update_subjects(self, subjects: List[str]):
        for teaching in self.teachings:
            if teaching.subject_id not in subjects:
                db.session.delete(teaching)

        db.session.commit()

        for subject in subjects:
            if Teaching.query.filter_by(
                subject_id=subject, teacher_id=self.uid
            ).first():
                continue

            teaching = Teaching()
            teaching.teacher_id = self.uid
            teaching.subject_id = subject

            db.session.add(teaching)

        db.session.commit()

    def __repr__(self):
        return f"<Teacher {self.user.full_name} ID={self.uid}>"
