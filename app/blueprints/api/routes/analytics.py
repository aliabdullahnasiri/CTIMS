import json
from datetime import datetime, timedelta

from flask import Response
from flask_login import login_required
from sqlalchemy import func

from app.blueprints.api import bp
from app.extensions import db
from app.models.view import View


@bp.get("/analytics/weekly-views")
@login_required
def weekly_views() -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})

    today = datetime.now().date()
    week_ago = today - timedelta(days=6)

    results = (
        db.session.query(
            func.date(View.created_at).label("date"),
            func.count(View.id).label("views"),
        )
        .filter(View.created_at >= week_ago)
        .group_by(func.date(View.created_at))
        .order_by(func.date(View.created_at))
        .all()
    )

    x = []
    y = []

    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_str = day.strftime("%a")

        count = next((r.views for r in results if r.date == day), 0)

        x.append(day_str)
        y.append(count)

    response.response = json.dumps(dict(zip(x, y)))
    response.status_code = 200

    return response
