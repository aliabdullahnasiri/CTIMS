from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import department, employee, job, time, upload, user
