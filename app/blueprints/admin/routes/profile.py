from flask import render_template
from flask_login import current_user

from app.blueprints.admin import bp
from app.forms.user import UpdateUserForm


@bp.get("/profile")
def profile():
    form = UpdateUserForm()

    return render_template(
        "admin/pages/profile.html",
        title="Profile",
        user=current_user,
        update_user_form=form,
    )
