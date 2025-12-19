from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import (
    attendance,
    class_,
    department,
    employee,
    exam,
    job,
    result,
    semester,
    student,
    subject,
    teacher,
    time,
    upload,
    user,
)
