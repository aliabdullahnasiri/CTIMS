from flask import Response

from app.blueprints.api import bp


@bp.get("/export/student/<string:uid>/registration-form")
def export_student_registration_form(uid: str) -> Response:
    response: Response = Response()

    return response
