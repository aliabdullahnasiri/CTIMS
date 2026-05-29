from flask import render_template

from app.blueprints.admin import bp
from app.forms.class_ import AddClassForm, UpdateClassForm
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/classes")
@permission_required(Permission.get("FETCH_CLASSES") | Permission.get("FETCH_CLASS"))
def classes():
    return render_template(
        "admin/pages/classes.html",
        title="Classes",
        form={"a": AddClassForm(), "u": UpdateClassForm()},
    )
