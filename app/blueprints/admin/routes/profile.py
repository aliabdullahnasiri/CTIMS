from flask import render_template
from flask_babel import gettext as _
from flask_login import current_user, login_required

from app.blueprints.admin import bp
from app.forms.profile import UpdateProfileForm


@bp.get("/profile")
@login_required
def profile():
    return render_template(
        "admin/pages/profile.html",
        title=_("Profile"),
        user=current_user,
        update_user_form=UpdateProfileForm(),
    )
