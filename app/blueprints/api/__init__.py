from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import (
    class_,
    department,
    employee,
    job,
    semester,
    student,
    subject,
    teacher,
    time,
    upload,
    user,
)
