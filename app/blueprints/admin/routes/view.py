import json
from typing import Dict

from flask import Response, current_app, render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.config import Config
from app.func import validate_uid
from app.models.class_ import Class
from app.models.daily_section import DailySection
from app.models.department import Department
from app.models.employee import Employee
from app.models.exam import Exam
from app.models.job import Job
from app.models.permission import Permission
from app.models.role import Role
from app.models.semester import Semester
from app.models.student import Student
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.time import Time

entities: Dict = {
    "time": Time,
    "department": Department,
    "semester": Semester,
    "job": Job,
    "employee": Employee,
    "teacher": Teacher,
    "subject": Subject,
    "class": Class,
    "student": Student,
    "exam": Exam,
    "permission": Permission,
    "role": Role,
    "daily_section": DailySection,
}


@bp.get("/view/<string:entity>/<string:uid>")
def view(entity: str, uid: str) -> Response:
    response: Response = Response()

    obj = entities.get(entity)

    if not validate_uid(uid) or not obj:
        response.headers.setdefault("Content-Type", "application/json")
        response.response = json.dumps({"error": _("INVALID_UID_ENTITY_ERROR")})
        response.status_code = 404

        return response

    for template in Config.VIEWS_TEMPS:
        filename = template.name

        if filename.startswith(entity):
            with open(template) as f:
                if row := obj.query.filter_by(uid=uid).first():
                    template = current_app.jinja_env.from_string(f.read())
                    response.response = render_template(template, **{entity: row})
                    response.status_code = 200
                else:
                    response.response = json.dumps(
                        {"error": _("ROW_WAS_NOT_FOUND_MSG")}
                    )
                    response.status_code = 404
            break
    else:
        response.response = json.dumps({"error": _("TEMPLATE_WAS_NOT_FOUND_MSG")})
        response.status_code = 404

    return response
