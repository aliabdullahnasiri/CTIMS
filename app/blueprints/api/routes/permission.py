import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.permission import UpdatePermissionForm
from app.func import render_td
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("name"), ColumnName(g("NAME_LABEL"))),
]


@bp.get("/fetch/permissions")
@permission_required(Permission.get("FETCH_PERMISSIONS"))
def fetch_permissions() -> Response:
    permissions: List[Dict] = [
        permission.to_dict() for permission in Permission.query.all()
    ]

    return Response(
        json.dumps(permissions),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/permissions")
@permission_required(Permission.get("FETCH_PERMISSIONS"))
def fetch_permissions_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    permissions: List[Permission] = Permission.query.all()
    rows: List[List] = []

    for permission in permissions:
        row = [render_td(col_id, permission) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": [(col_id, g(col_name)) for col_id, col_name in cols],
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/permission/<string:uid>")
@permission_required(Permission.get("FETCH_PERMISSION"))
def fetch_permission_row(uid: str) -> Response:
    permission: Union[Permission, None] = Permission.query.filter_by(uid=uid).first()

    if permission:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, permission) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("PERMISSION_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/permission/<string:uid>")
@permission_required(Permission.get("FETCH_PERMISSION"))
def fetch_permission(uid: str) -> Response:
    permission: Union[Permission, None] = Permission.query.filter_by(uid=uid).first()

    if permission:
        return Response(
            json.dumps(permission.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("PERMISSION_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/permission")
@permission_required(
    Permission.get("FETCH_PERMISSION") | Permission.get("UPDATE_PERMISSION")
)
def update_permission() -> Response:
    response: Dict = {}

    form = UpdatePermissionForm()

    if form.validate_on_submit():
        uid = form.uid.data

        permission: Union[Permission, None] = Permission.query.filter_by(
            uid=uid
        ).first()

        if permission:
            permission.name = form.name.data
            permission.description = form.description.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("PERMISSION_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = g("SUCCESS_SUCCESS_MSG")
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("PERMISSION_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )
