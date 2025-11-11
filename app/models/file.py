import pathlib
from datetime import datetime, timezone
from typing import Optional, Self

import humanize

from app.constants import APP_DIR
from app.extensions import db


class FileMixin(object):
    pass


class File(db.Model):
    __tablename__ = "files"

    # File Info
    file_name = db.Column(
        db.String(255),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).date(),
    )
    file_description = db.Column(db.String(255))
    file_for = db.Column(db.String(25))
    file_url = db.Column(db.String(255), nullable=False)

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

    def to_dict(self) -> dict:
        return {
            "file_id": self.uid,
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


class TeacherFile(db.Model):
    __tablename__ = "teacher_files"

    teacher_id = db.Column(db.String(8), db.ForeignKey("teachers.uid"), nullable=False)
    file_id = db.Column(
        db.String(8), db.ForeignKey("files.uid"), nullable=False, unique=True
    )

    file = db.relationship("File")
    teacher = db.relationship("Teacher", back_populates="files")

    def __repr__(self):
        return f"<TeachertFile ID={self.uid} TeacherID={self.teacher_id} FileID={self.file_id}>"


class SubjectFile(db.Model):
    __tablename__ = "subject_files"

    subject_id = db.Column(db.String(8), db.ForeignKey("subjects.uid"), nullable=False)
    file_id = db.Column(
        db.String(8), db.ForeignKey("files.uid"), nullable=False, unique=True
    )

    file = db.relationship("File")
    subject = db.relationship("Subject", back_populates="files")

    def __repr__(self):
        return f"<SubjectFile ID={self.uid} SubjectID={self.subject_id} FileID={self.file_id}>"


class StudentFile(db.Model):
    __tablename__ = "student_files"

    student_id = db.Column(db.String(8), db.ForeignKey("students.uid"), nullable=False)
    file_id = db.Column(
        db.String(8), db.ForeignKey("files.uid"), nullable=False, unique=True
    )

    file = db.relationship("File")
    student = db.relationship("Student", back_populates="files")

    def __repr__(self):
        return f"<StudentFile ID={self.uid} StudentID={self.student_id} FileID={self.file_id}>"
