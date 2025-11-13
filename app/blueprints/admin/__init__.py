from flask import Blueprint, redirect, url_for

bp = Blueprint("admin", __name__)

from .routes import dashboard, department, employee, job, time, user
