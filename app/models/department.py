from typing import Dict

from app.extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    name = db.Column(db.String(60))
    description = db.Column(db.String(255))
    manager = db.Column(db.String(8))

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Department {self.name}>"
