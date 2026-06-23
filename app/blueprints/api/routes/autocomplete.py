from flask import render_template, request
from flask_login import login_required

from app.blueprints.api import bp
from app.models.base import Base


@bp.get("/autocomplete")
@login_required
def autocomplete() -> str:
    query = request.args.get("query")
    model_name = request.args.get("model-name")
    search_col = request.args.get("search-col")
    limit = int(request.args.get("limit", 10))
    template = request.args.get("template")

    for cls in Base.__subclasses__():
        if cls.__name__ == model_name and search_col:
            column = getattr(cls, search_col)

            return render_template(
                f"admin/autocomplete/{template}",
                rows=(
                    cls.query.filter(column.ilike(f"%{query}%")).limit(limit).all()
                    if query
                    else cls.query.limit(limit).all()
                ),
            )

    return ""
