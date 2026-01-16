from flask import render_template

from app.blueprints.admin import bp
from app.forms.class_ import AddClassForm, UpdateClassForm


@bp.get("/classes")
def classes():
    return render_template(
        "admin/pages/classes.html",
        title="Classes",
        form={"a": AddClassForm(), "u": UpdateClassForm()},
    )
