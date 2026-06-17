from operator import call

from app.extensions.db import db


class IdentityCardType:
    ELECTRONIC = "electronic"
    PAPER = "paper"


class Student(db.Model):
    __tablename__ = "students"

    base_number = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.String(8), db.ForeignKey("users.uid"), nullable=False)
    class_id = db.Column(db.String(8), db.ForeignKey("classes.uid"))
    daily_section_uid = db.Column(
        db.String(8),
        db.ForeignKey("daily_sections.uid"),
    )

    father_name = db.Column(db.String(255))
    grandfather_name = db.Column(db.String(255))

    electronic_tazkira_number = db.Column(db.String(100), unique=True)

    tazkira_folder = db.Column(db.String(50), nullable=True)
    tazkira_page_number = db.Column(db.String(50), nullable=True)
    tazkira_registration_number = db.Column(db.String(50), nullable=True)
    tazkira_sakok_number = db.Column(db.String(50), nullable=True)

    permanent_province_uid = db.Column(
        db.String(8),
        db.ForeignKey("province.uid"),
    )

    permanent_district_uid = db.Column(
        db.String(8),
        db.ForeignKey("district.uid"),
    )
    permanent_village = db.Column(db.String(255))

    current_province_uid = db.Column(
        db.String(8),
        db.ForeignKey("province.uid"),
    )

    current_district_uid = db.Column(
        db.String(8),
        db.ForeignKey("district.uid"),
    )
    current_village = db.Column(db.String(255))

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
            "base_number": self.base_number,
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
