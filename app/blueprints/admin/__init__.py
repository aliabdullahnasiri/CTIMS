from flask import Blueprint, redirect, url_for

bp = Blueprint("admin", __name__)

from .routes import (
    class_,
    dashboard,
    department,
    employee,
    job,
    profile,
    semester,
    student,
    subject,
    teacher,
    time,
    user,
)
