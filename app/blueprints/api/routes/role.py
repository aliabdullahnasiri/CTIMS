import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.role import AddRoleForm, UpdateRoleForm
from app.func import render_td
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("is_deletable"), ColumnName("IS_DELETABLE")),
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("name"), ColumnName("Name")),
]


@bp.get("/fetch/roles")
@login_required
@permission_required(Permission.get("FETCH_ROLES"))
def fetch_roles() -> Response:
    roles: List[Dict] = [role.to_dict() for role in Role.query.all()]

    return Response(
        json.dumps(roles),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/roles")
@login_required
@permission_required(Permission.get("FETCH_ROLES"))
def fetch_roles_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    roles: List[Role] = Role.query.all()
    rows: List[List] = []

    for role in roles:
        row = [render_td(col_id, role) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/role/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_ROLE"))
def fetch_role_row(uid: str) -> Response:
    role: Union[Role, None] = Role.query.filter_by(uid=uid).first()

    if role:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, role) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Role with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/role/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_ROLE"))
def fetch_role(uid: str) -> Response:
    role: Union[Role, None] = Role.query.filter_by(uid=uid).first()

    if role:
        return Response(
            json.dumps(role.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Role with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/role")
@login_required
@permission_required(Permission.get("UPDATE_ROLE"))
def update_role() -> Response:
    response: Dict = {}

    form = UpdateRoleForm()

    if form.validate_on_submit():
        uid = form.uid.data

        role: Union[Role, None] = Role.query.filter_by(uid=uid).first()

        if role:
            dct = role.to_dict()
            readonly = dct["readonly"]

            role.description = form.description.data

            if "default" not in readonly:
                role.default = form.default.data

            if "permissions" not in readonly and (permissions := form.permissions.data):
                try:
                    permissions = json.loads(permissions)

                    for p in role.permissions.all():
                        if p.uid not in permissions:
                            role.permissions.remove(p)

                    for permission in permissions:
                        if (
                            obj := Permission.query.filter_by(uid=permission).scalar()
                        ) not in role.permissions:
                            role.permissions.add(obj)
                except json.JSONDecodeError as err:
                    print("ERROR: ", err)

            db.session.commit()

            for user in role.users.all():
                dct.remove(user.id)

            response["title"] = "Updated!"
            response["category"] = "success"
            response["message"] = "Role updated successfully!"
        else:
            response["title"] = "Not Found"
            response["category"] = "error"
            response["message"] = "Role record not found."
    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/role/<string:uid>")
@login_required
@permission_required(Permission.get("DELETE_ROLE"))
def delete_role(uid: str):
    response = {}

    if role := Role.query.filter_by(uid=uid).scalar():
        if not role.primary:
            db.session.delete(role)
            db.session.commit()

            response["title"] = "Deleted!"
            response["message"] = "Role has been deleted successfully."
            response["category"] = "success"
            response["status"] = 200
        else:
            response["title"] = "Warning!"
            response["message"] = "Primary roles cannot be deleted."
            response["category"] = "success"
            response["status"] = 403

    else:
        response["title"] = "Error :("
        response["message"] = "User not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/role")
@login_required
@permission_required(Permission.get("CREATE_ROLE"))
def add_role():
    form = AddRoleForm()

    response: Dict = {}

    if form.validate_on_submit():
        role: Role = Role()

        role.name = form.name.data
        role.description = form.description.data
        role.default = form.default.data
        role.primary = False

        db.session.add(role)
        db.session.commit()

        if permissions := form.permissions.data:
            permissions = [
                Permission.query.filter_by(uid=permission).scalar()
                for permission in json.loads(permissions)
            ]

            for permission in permissions:
                if permission not in role.permissions:
                    role.permissions.append(permission)

        db.session.commit()

        response["message"] = "User added successfully"
        response["category"] = "success"
        response["title"] = "User Added"
        response["id"] = getattr(role, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
