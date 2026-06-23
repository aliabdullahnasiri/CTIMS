from operator import call

from flask_babel import gettext as _
from sqlalchemy import func

from app.extensions.db import db
from app.models.subject import StudentSubject


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

    kankor_id = db.Column(
        db.String(12),
        unique=True,
        nullable=True,
        index=True,
        comment="Kankor registration number",
    )

    kankor_year = db.Column(db.SmallInteger, nullable=True, comment="Kankor exam year")

    kankor_score = db.Column(db.Float, nullable=True, comment="Kankor score")

    kankor_rank = db.Column(db.Integer, nullable=True, comment="Kankor rank")

    kankor_result = db.Column(
        db.String(100), nullable=True, comment="Faculty or department accepted"
    )

    kankor_university = db.Column(
        db.String(150), nullable=True, comment="Accepted university"
    )

    kankor_province = db.Column(db.String(100), nullable=True, comment="Exam province")

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

    high_school_name = db.Column(
        db.String(255), nullable=True, comment="High School Name"
    )

    high_school_registration_no = db.Column(
        db.String(100), nullable=True, comment="High School Registration Number"
    )

    high_school_province_uid = db.Column(
        db.String(8),
        db.ForeignKey("province.uid"),
    )

    high_school_graduation_year = db.Column(
        db.Integer, nullable=True, comment="Graduation Year"
    )

    father_job = db.Column(db.String(100), nullable=True)
    father_job_address = db.Column(db.String(100), nullable=True)

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

    current_province = db.relationship(
        "Province",
        foreign_keys=[current_province_uid],
        backref=db.backref("students_current_province", lazy="dynamic"),
    )
    permanent_province = db.relationship(
        "Province",
        foreign_keys=[permanent_province_uid],
        backref=db.backref("students_permanent_province", lazy="dynamic"),
    )
    current_district = db.relationship(
        "District",
        foreign_keys=[current_district_uid],
        backref=db.backref("students_current_district", lazy="dynamic"),
    )
    permanent_district = db.relationship(
        "District",
        foreign_keys=[permanent_district_uid],
        backref=db.backref("students_permanent_district", lazy="dynamic"),
    )
    high_school_province = db.relationship(
        "Province",
        foreign_keys=[high_school_province_uid],
    )

    def to_dict(self) -> dict:
        grade_stat = (
            db.session.query(
                StudentSubject.grade_uid,
                func.sum(StudentSubject.score).label("total"),
                func.avg(StudentSubject.score).label("average"),
            )
            .filter(StudentSubject.student_uid == getattr(self, "uid"))
            .group_by(StudentSubject.grade_uid)
            .all()
        )

        return (
            {
                "base_number": self.base_number,
                "kankor_id": self.kankor_id,
                "electronic_tazkira_number": self.electronic_tazkira_number,
                "identity_card_type": (
                    IdentityCardType.ELECTRONIC
                    if self.electronic_tazkira_number
                    else IdentityCardType.PAPER
                ),
                "tazkira_folder": self.tazkira_folder,
                "tazkira_page_number": self.tazkira_page_number,
                "tazkira_registration_number": self.tazkira_registration_number,
                "tazkira_sakok_number": self.tazkira_sakok_number,
                "permanent_province": self.permanent_province_uid,
                "permanent_district": self.permanent_district_uid,
                "permanent_village": self.permanent_village,
                "current_province": self.current_province_uid,
                "current_district": self.current_district_uid,
                "current_village": self.current_village,
                "father_name": self.father_name,
                "grandfather_name": self.grandfather_name,
                "daily_section_uid": self.daily_section_uid,
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
                "high_school_name": self.high_school_name,
                "high_school_registration_no": self.high_school_registration_no,
                "high_school_graduation_year": self.high_school_graduation_year,
                "admission_date": (
                    self.daily_section.academic_year if self.daily_section else None
                ),
                "high_school_last_grade": 12,
                "birthday_year": (
                    self.user.birthday.year if self.user.birthday else "0000"
                ),
                "current_province_name": (
                    _(self.current_province.name) if self.current_province else ""
                ),
                "current_district_name": (
                    _(self.current_district.name) if self.current_district else ""
                ),
                "permanent_district_name": (
                    _(self.permanent_district.name) if self.permanent_district else ""
                ),
                "permanent_province_name": (
                    _(self.permanent_province.name) if self.permanent_province else ""
                ),
                "father_job": self.father_job,
                "father_job_address": self.father_job_address,
                "high_school_province": self.high_school_province_uid,
                "high_school_province_name": (
                    _(self.high_school_province.name)
                    if self.high_school_province_uid
                    else None
                ),
                **call(getattr(super(), "to_dict")),
            }
            | {
                f"GRADE_{s.grade_uid}_{s.subject_uid}": s.score
                for s in getattr(self, "school_scores").all()
            }
            | {
                f"GRADE_{uid}_SUM": round(val)
                for uid, val, _ in grade_stat
                if isinstance(val, (int, float))
            }
            | {
                f"GRADE_{uid}_AVG": round(val)
                for uid, _, val in grade_stat
                if isinstance(val, (int, float))
            }
        )

    def __repr__(self):
        return f"<Student full_name={self.user.full_name!r}>"
