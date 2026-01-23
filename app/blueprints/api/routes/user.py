import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms.user import AddUserForm, UpdateUserForm
from app.functions import render_td
from app.models.permission import Permission
from app.models.user import User, permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_user"), ColumnName("User")),
    (ColumnID("user_name"), ColumnName("User Name")),
    (ColumnID("birthday"), ColumnName("Birthday")),
    (ColumnID("age"), ColumnName("Age")),
]


@bp.get("/fetch/users")
@login_required
@permission_required(Permission.get("FETCH_USERS"))
def fetch_users() -> Response:
    users: List[User] = [user.to_dict() for user in User.query.all()]

    response: Response = Response(
        json.dumps(users), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/users")
@login_required
@permission_required(Permission.get("FETCH_USERS"))
def fetch_users_rows() -> Response:
    users: List[User] = User.query.all()

    rows: List[List] = []

    for user in users:
        row = [render_td(col_id, user) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response: Response = Response(
        json.dumps(dct),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/row/user/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_USER"))
def fetch_user_row(uid) -> Response:
    response: Response = Response()

    user: Union[User, None] = User.query.filter_by(uid=uid).first()

    if user:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, user) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "User with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/user/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_USER"))
def fetch_user(uid) -> Response:
    user = User.query.filter_by(uid=uid).first()

    if user:
        response: Response = Response(
            json.dumps(user.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "User with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/user")
@login_required
@permission_required(Permission.get("FETCH_USER") | Permission.get("UPDATE_USER"))
def update_user() -> Response:
    form = UpdateUserForm()

    response: Dict = {}

    if form.validate_on_submit():
        user = User.query.filter_by(uid=form.uid.data).first()

        if user:
            user.first_name = form.first_name.data
            user.middle_name = form.middle_name.data
            user.last_name = form.last_name.data
            user.user_name = form.user_name.data
            user.email = form.email.data
            user.birthday = form.birthday.data

            if files := request.form.get("files"):
                try:
                    user.update_files(json.loads(files))
                except json.JSONDecodeError as err:
                    console.print(err)

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "User updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/user/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_USER") | Permission.get("DELETE_USER"))
def delete_user(uid):
    response = {}

    if user := User.query.filter_by(uid=uid).first():
        db.session.delete(user)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "User deleted successfully"
        response["category"] = "success"
        response["status"] = 200

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


@bp.post("/add/user")
@login_required
@permission_required(Permission.get("CREATE_USER"))
def add_user() -> Response:
    form = AddUserForm()

    response: Dict = {}

    if form.validate_on_submit():
        user = User()

        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.user_name = form.user_name.data
        user.email = form.email.data
        user.birthday = form.birthday.data

        if form.phones.data:
            user.update_phones(json.loads(form.phones.data))

        if files := request.form.get("files"):
            try:
                user.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        if passwd := form.password.data:
            user.set_password(passwd)

        user.update_roles()

        db.session.add(user)
        db.session.commit()

        response["message"] = "User added successfully"
        response["category"] = "success"
        response["title"] = "User Added"
        response["id"] = user.uid

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
