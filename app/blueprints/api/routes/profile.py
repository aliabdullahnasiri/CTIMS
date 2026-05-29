import json
from typing import Dict

from flask import Response, request
from flask_login import current_user, login_required

from app.blueprints.api import bp
from app.extensions.console import console
from app.extensions.db import db
from app.forms.profile import UpdateProfileForm
from app.models.role import Role


@bp.get("/fetch/profile")
@login_required
def fetch_profile():
    response: Response = Response(
        json.dumps(current_user.to_dict()),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.post("/update/profile")
@login_required
def update_profile():
    form = UpdateProfileForm()

    response: Dict = {}

    if form.validate_on_submit():
        user = current_user
        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.user_name = form.user_name.data
        user.email = form.email.data
        user.birthday = form.birthday.data

        if passwd := form.password.data:
            user.set_password(passwd)

        if files := request.form.get("files"):
            try:
                user.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        if form.phones.data:
            user.update_phones(json.loads(form.phones.data))

        if form.roles.data:
            user.update_roles(
                [
                    role
                    for uid in json.loads(form.roles.data)
                    if (role := Role.query.filter_by(uid=uid).scalar())
                ]
            )

        db.session.commit()

        response["title"] = "Good job!"
        response["category"] = "success"
        response["message"] = "User updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )
