from app.extensions import db
from app.models.file import File


class Student(db.Model):
    __tablename__ = "students"

    user_id = db.Column(db.String(8), db.ForeignKey("users.uid"))
    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"))

    attendances = db.relationship(
        "StudentAttendance",
        back_populates="student",
        cascade="all, delete, delete-orphan",
    )
    class_ = db.relationship("Class", back_populates="students")
    results = db.relationship(
        "Result", back_populates="student", cascade="all, delete, delete-orphan"
    )

    user = db.relationship("User", cascade="delete")

    @property
    def files(self):
        return [file for file in File.query.filter_by(file_for=self.user.uid).all()]

    def to_dict(self) -> dict:
        return {
            "user_uid": self.user.uid,
            "class_id": self.class_id,
            "first_name": self.user.first_name,
            "middle_name": self.user.middle_name,
            "last_name": self.user.last_name,
            "full_name": self.user.full_name,
            "email": self.user.email,
            "birthday": self.user.display_birthday,
            "age": self.user.age,
            "avatar": self.user.avatar_path,
            "phones": [phone.number for phone in self.user.phones],
            "files": [f.to_dict() for f in self.files],
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Student {self.user.full_name} ID={self.uid}>"
