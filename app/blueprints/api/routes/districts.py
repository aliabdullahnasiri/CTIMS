import json
from typing import Dict, List

from flask import Response, request

from app.blueprints.api import bp
from app.models.district import District


@bp.get("/fetch/districts")
def fetch_districts() -> Response:
    province_uid = request.args.get("uid")
    query = District.query
    districts: List[Dict] = [
        district.to_dict()
        for district in (
            query.filter_by(province_uid=province_uid) if province_uid else query.all()
        )
    ]

    return Response(
        json.dumps(districts),
        status=200,
        headers={"Content-Type": "application/json"},
    )
