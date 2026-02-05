import json
from datetime import datetime, timedelta

from flask import Response
from flask_login import login_required
from sqlalchemy import extract, func

from app.blueprints.api import bp
from app.extensions import db
from app.models.class_ import Class
from app.models.student import Student
from app.models.user import User
from app.models.view import View


@bp.get("/analytics/weekly/<int:index>")
@login_required
def weekly(index: int) -> Response:
    models = [View, User]
    model = models.__getitem__(index if index < len(models) else 0)

    response: Response = Response(headers={"Content-Type": "application/json"})

    today = datetime.now().date()
    week_ago = today - timedelta(days=6)

    results = (
        db.session.query(
            func.date(model.created_at).label("date"),
            func.count(model.id).label(name := model.__table__.name),
        )
        .filter(model.created_at >= week_ago)
        .group_by(func.date(model.created_at))
        .order_by(func.date(model.created_at))
        .all()
    )

    x = []
    y = []

    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_str = day.strftime("%a")

        count = next((r.__getattr__(name) for r in results if r.date == day), 0)

        x.append(day_str)
        y.append(count)

    response.response = json.dumps(dict(zip(x, y)))
    response.status_code = 200

    return response


@bp.get("/analytics/yearly/<int:index>")
@login_required
def yearly(index: int) -> Response:
    models = [Student, Class]
    model = models.__getitem__(index if index < len(models) else 0)

    response: Response = Response(headers={"Content-Type": "application/json"})
    today = datetime.now().date()
    year_ago = today.replace(day=1) - timedelta(days=365)

    results = (
        db.session.query(
            func.concat(extract("year", model.created_at))
            .concat(chr(45))
            .concat(extract("month", model.created_at))
            .label("month"),
            func.count(model.uid).label("students"),
        )
        .filter(model.created_at >= year_ago)
        .filter(model.created_at < today.replace(day=1))
        .group_by("month")
        .all()
    )

    conv = lambda date, format: datetime(
        *map(int, date.split(chr(45))), day=1
    ).strftime(format)

    data = {conv(r.month, "%Y-%m"): r.students for r in results}

    increment = timedelta(31)

    while year_ago < today:
        data.setdefault(year_ago.strftime("%Y-%m"), 0)
        year_ago += increment

    data = {
        conv(month, "%b %y"): data.get(month)
        for month in sorted(data, key=lambda month: month)
    }

    response.response = json.dumps(data)
    response.status_code = 200

    return response
