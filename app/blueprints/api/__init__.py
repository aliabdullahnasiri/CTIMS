from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import (
    class_,
    department,
    employee,
    job,
    semester,
    subject,
    teacher,
    time,
    upload,
    user,
)
