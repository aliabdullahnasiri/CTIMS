from flask import render_template
from flask_babel import gettext as _

from app.blueprints.admin import bp
from app.forms.daily_section import AddDailySectionForm, UpdateDailySectionForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/daily_sections")
@permission_required(
    Permission.get("FETCH_DAILY_SECTIONS") | Permission.get("FETCH_DAILY_SECTION")
)
def daily_sections():
    return render_template(
        "admin/pages/daily_sections.html",
        title=_("DAILY_SECTIONS_LABEL"),
        form={"a": AddDailySectionForm(), "u": UpdateDailySectionForm()},
    )
