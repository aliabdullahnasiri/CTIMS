import enum
from datetime import datetime, timezone
from operator import call

from app.extensions import db


class AttendanceStatus(enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"


class StudentAttendance(db.Model):
    __tablename__ = "student_attendance"

    student_id = db.Column(db.String(8), db.ForeignKey("students.uid"), nullable=False)
    date = db.Column(
        db.Date, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    time = db.Column(db.Time(), default=lambda: datetime.now().time())
    status = db.Column(db.Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    student = db.relationship("Student", back_populates="attendances")

    def to_dict(self):
        return {
            "date": self.display_date,
            "time": self.display_time,
            "status": self.status.value,
            "student": self.student.to_dict(),
            **call(getattr(super(), "to_dict")),
        }

    @property
    def display_date(self) -> str:
        return self.date.strftime("%Y-%m-%d") if self.date else "N/A"

    @property
    def display_time(self) -> str:
        return self.time.strftime("%H:%M:%S") if self.time else "N/A"

    def __repr__(self):
        return f"<StudentAttendance StudentID={self.student_id}>"


class TeacherAttendance(db.Model):
    __tablename__ = "teacher_attendance"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    date = db.Column(
        db.Date,
        default=lambda: datetime.now(timezone.utc),
    )
    time = db.Column(db.Time(), default=lambda: datetime.now().time())
    status = db.Column(db.Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    teacher = db.relationship("Teacher", back_populates="attendances")

    def __repr__(self):
        return f"<TeacherAttendance TeacherID={self.teacher_id}>"

    def to_dict(self):
        return {
            "date": self.display_date,
            "time": self.display_time,
            "status": self.status.value,
            "teacher": self.teacher.to_dict(),
            **call(getattr(super(), "to_dict")),
        }

    @property
    def display_date(self) -> str:
        return self.date.strftime("%Y-%m-%d") if self.date else "N/A"

    @property
    def display_time(self) -> str:
        return self.time.strftime("%H:%M:%S") if self.time else "N/A"
