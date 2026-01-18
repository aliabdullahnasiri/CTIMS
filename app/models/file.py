import pathlib
from datetime import datetime, timezone
from typing import Optional, Self

import humanize

from app.constants import APP_DIR
from app.extensions import db


class File(db.Model):
    __tablename__ = "files"

    uid = None
    user_id = db.Column(db.String(8), db.ForeignKey("users.uid"), nullable=False)

    # File Info
    file_name = db.Column(
        db.String(255),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).date(),
    )
    file_description = db.Column(db.String(255))
    file_for = db.Column(db.String(8))
    file_url = db.Column(db.String(255), nullable=False)

    user = db.relationship("User", back_populates="files")

    @property
    def path(self: Self) -> pathlib.Path:
        return pathlib.Path(f"{APP_DIR}/{self.file_url}")

    @property
    def exists(self: Self) -> bool:
        return self.path.exists()

    @property
    def size(self: Self) -> int:
        try:
            return self.path.stat().st_size if self.exists else 0
        except OSError:
            return 0

    @property
    def human_size(self: Self) -> str:
        return humanize.naturalsize(self.size) if self.size else "0 B"

    @property
    def extension(self: Self) -> Optional[str]:
        return self.path.suffix.lstrip(".").upper() if self.path.suffix else None

    @property
    def display_name(self: Self) -> str:
        return (
            f"{self.file_name}.{self.extension.lower()}"
            if self.extension
            else self.file_name
        )

    @property
    def display_file_name(self):
        s = slice(0, 15)
        n = self.file_name

        if len(n) > 15:
            return f"{n[s]}...{n[-15:]}"

        return self.file_name

    @property
    def display_file_description(self):
        return self.file_description or "N/A"

    @property
    def display_file_for(self):
        return self.file_for or "N/A"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_description": self.file_description,
            "file_for": self.file_for,
            "file_url": self.file_url,
            "extension": self.extension,
            "size": self.size,
            "human_size": self.human_size,
            "exists": self.exists,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<File {self.file_name} ({self.human_size}) ID={self.file_id}>"
