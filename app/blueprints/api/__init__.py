from flask import Blueprint

bp = Blueprint("api", __name__)

from .routes import department, time, upload, user
