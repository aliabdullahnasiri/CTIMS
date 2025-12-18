from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import (
    class_,
    department,
    employee,
    exam,
    job,
    semester,
    student,
    subject,
    teacher,
    time,
    upload,
    user,
)
