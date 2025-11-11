from app.extensions import db


class EmployeePhone(db.Model):
    __tablename__ = "employee_phones"

    employee_id = db.Column(
        db.String(8), db.ForeignKey("employees.uid"), nullable=False
    )
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    employee = db.relationship("Employee", back_populates="phones")

    def to_dict(self) -> dict:
        return {
            "employee_id": self.uid,
            "phone_number": self.phone_number,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<EmployeePhone {self.phone_number} Employee={self.employee_id}>"


class TeacherPhone(db.Model):
    __tablename__ = "teacher_phones"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    teacher = db.relationship("Teacher", back_populates="phones")

    def to_dict(self) -> dict:
        return {
            "teacher_id": self.teacher_id,
            "phone_number": self.phone_number,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<TeacherPhone {self.phone_number} Teacher={self.teacher_id}>"


class StudentPhone(db.Model):
    __tablename__ = "student_phones"

    student_id = db.Column(db.String(8), db.ForeignKey("students.uid"), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    student = db.relationship("Student", back_populates="phones")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the StudentPhone."""
        return {
            "phone_id": self.uid,
            "student_id": self.student_id,
            "phone_number": self.phone_number,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<StudentPhone {self.phone_number} Student={self.student_id}>"
