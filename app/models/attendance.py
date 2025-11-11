import enum
from datetime import datetime, timezone

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
    status = db.Column(db.Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    student = db.relationship("Student", back_populates="attendances")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "status": self.status.value,
            "student": self.student.to_dict(),
            **super().to_dict(),
        }

    @property
    def display_date(self) -> str:
        return self.date.strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<StudentAttendance {self.uid} StudentID={self.student_id}>"


class TeacherAttendance(db.Model):
    __tablename__ = "teacher_attendance"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    date = db.Column(
        db.Date,
        default=lambda: datetime.now(timezone.utc),
    )
    status = db.Column(db.Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    teacher = db.relationship("Teacher", back_populates="attendances")

    def __repr__(self):
        return f"<TeacherAttendance {self.uid} TeacherID={self.teacher_id}>"

    def to_dict(self):
        return {
            "attendance_id": self.uid,
            "date": self.display_date,
            "status": self.status.value,
            "teacher": self.teacher.to_dict(),
        }

    @property
    def display_date(self) -> str:
        return self.date.strftime("%Y-%m-%d")
