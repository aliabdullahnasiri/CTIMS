import json
from typing import Dict

from flask import Response, current_app, render_template

from app.blueprints.admin import bp
from app.config import Config
from app.functions import validate_uid
from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job
from app.models.semester import Semester
from app.models.time import Time

entities: Dict = {
    "time": Time,
    "department": Department,
    "semester": Semester,
    "job": Job,
    "employee": Employee,
}


@bp.get("/view/<string:entity>/<string:uid>")
def view(entity: str, uid: str) -> Response:
    response: Response = Response()

    obj = entities.get(entity)

    if not validate_uid(uid) or not obj:
        response.headers.setdefault("Content-Type", "application/json")
        response.response = json.dumps({"error": "Invalid UID/Entity :("})
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
                    response.response = json.dumps({"error": "Row was not found :("})
                    response.status_code = 404
            break
    else:
        response.response = json.dumps({"error": "Template was not found :("})
        response.status_code = 404

    return response
