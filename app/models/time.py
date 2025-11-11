from typing import Dict

from app.extensions import db


class Time(db.Model):
    __tablename__ = "times"

    title = db.Column(db.String(50))
    description = db.Column(db.String(255))

    start = db.Column(db.Time, nullable=True)
    end = db.Column(db.Time, nullable=True)

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
        return self.start_time.strftime("%H:%M") if self.start_time else "N/A"

    @property
    def display_end_time(self) -> str:
        return self.end_time.strftime("%H:%M") if self.end_time else "N/A"
