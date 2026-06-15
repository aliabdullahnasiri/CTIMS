import json
from typing import Dict, Union

from flask import Response

from app.blueprints.api import bp
from app.extensions.db import db
from app.models.file import File
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/delete/file/<string:id>")
@permission_required(Permission.get("DELETE_FILE"))
def delete_file(id: int) -> Response:
    response: Dict = {}
    file: Union[File, None] = File.query.filter_by(id=id).scalar()

    if file:
        db.session.delete(file)
        db.session.commit()

    return Response(
        json.dumps(response),
        headers={"Content-Type": "application/json"},
    )
