import json
import re

from flask_wtf import FlaskForm
from wtforms import ValidationError

from app.extensions.db import db
from app.models.class_ import Class
from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job
from app.models.phone import Phone
from app.models.role import Permission, Role
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.time import Time
from app.models.user import User


class Form(FlaskForm):
    pass
