from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import department, employee, job, teacher, time, upload, user
