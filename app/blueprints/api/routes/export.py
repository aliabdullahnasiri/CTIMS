from flask import Response

from app.blueprints.api import bp


@bp.get("/export/daily-section/<string:uid>")
def export_daily_section(uid: str) -> Response:
    response: Response = Response()

    return response
