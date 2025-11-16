from flask import Blueprint, redirect, url_for

bp = Blueprint("admin", __name__)

from .routes import (
    attendance,
    class_,
    dashboard,
    department,
    employee,
    exam,
    job,
    profile,
    result,
    semester,
    student,
    subject,
    teacher,
    time,
    user,
)
