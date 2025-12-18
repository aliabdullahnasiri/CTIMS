from typing import Dict

from app.extensions import db


class Time(db.Model):
    __tablename__ = "times"

    title = db.Column(db.String(50))
    description = db.Column(db.String(255))

    start = db.Column(db.Time, nullable=True)
    end = db.Column(db.Time, nullable=True)

    classes = db.relationship("Class", back_populates="time")

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "start": self.display_start_time,
            "end": self.display_end_time,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<Time {self.title}>"

    @property
    def display_start_time(self) -> str:
        return self.start.strftime("%H:%M") if self.start else "N/A"

    @property
    def display_end_time(self) -> str:
        return self.end.strftime("%H:%M") if self.end else "N/A"
