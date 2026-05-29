from flask import render_template

from app.forms.user import AddUserForm, UpdateUserForm
from app.models.permission import Permission
from app.models.user import permission_required

from .. import bp


@bp.get("/users")
@permission_required(Permission.get("FETCH_USERS") | Permission.get("FETCH_USER"))
def users():
    update_user_form = UpdateUserForm()
    add_user_form = AddUserForm()

    return render_template(
        "admin/pages/users.html",
        title="Users",
        update_user_form=update_user_form,
        add_user_form=add_user_form,
    )
