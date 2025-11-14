from app.extensions import db


class Semester(db.Model):
    __tablename__ = "semesters"

    name = db.Column(db.String(50))
    number = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.String(8), db.ForeignKey("departments.uid"), nullable=False
    )

    department = db.relationship("Department", back_populates="semesters")
    subjects = db.relationship(
        "Subject", back_populates="semester", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "number": self.number,
            "department_uid": self.department_id,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Semester {self.name} ID={self.uid}>"
