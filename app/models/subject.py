from typing import Dict

from app.extensions import db


class Subject(db.Model):
    __tablename__ = "subjects"

    name = db.Column(db.String(50))
    description = db.Column(db.String(255))

    teachings = db.relationship(
        "Teaching", back_populates="subject", cascade="all, delete-orphan"
    )
    files = db.relationship(
        "SubjectFile", back_populates="subject", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "files": [f.file.to_dict() for f in self.files],
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Subject {self.name}>"
