from operator import call

from app.extensions.db import db


class Student(db.Model):
    __tablename__ = "students"

    user_id = db.Column(db.String(8), db.ForeignKey("users.uid"))
    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"))

    class_ = db.relationship("Class", back_populates="students")
    attendances = db.relationship(
        "StudentAttendance",
        back_populates="student",
        cascade="all, delete, delete-orphan",
    )
    results = db.relationship(
        "Result", back_populates="student", cascade="all, delete, delete-orphan"
    )

    user = db.relationship("User", cascade="delete")

    daily_section = db.relationship(
        "DailySection",
        back_populates="students",
    )

    def to_dict(self) -> dict:
        return {
            "user_uid": self.user.uid,
            "class_id": self.class_id,
            "first_name": self.user.first_name,
            "middle_name": self.user.middle_name,
            "last_name": self.user.last_name,
            "full_name": self.user.full_name,
            "user_name": self.user.user_name,
            "email": self.user.email,
            "birthday": self.user.display_birthday,
            "age": self.user.age,
            "avatar": self.user.avatar_path,
            "phones": [phone.number for phone in self.user.phones.all()],
            "files": [f.to_dict() for f in self.user.files.all()],
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Student full_name={self.user.full_name!r}>"
