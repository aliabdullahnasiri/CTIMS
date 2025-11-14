import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.class_ import AddClassForm, UpdateClassForm
from app.models.class_ import Class
from app.types import ColumnID, ColumnName


@bp.get("/fetch/classes")
@login_required
def fetch_classes() -> Response:
    class_s: List[Dict] = [class_.to_dict() for class_ in Class.query.all()]

    return Response(
        json.dumps(class_s),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/classes")
@login_required
def fetch_classes_rows() -> Response:
    class_s: List[Class] = Class.query.all()

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("uid"), ColumnName("UID")),
        (ColumnID("name"), ColumnName("Name")),
    ]

    rows: List[List] = []

    for class_ in class_s:
        dct = class_.to_dict()
        row = [dct.get(col_id, "N/A") for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/class/<string:uid>")
@login_required
def fetch_class_row(uid: str) -> Response:
    class_: Union[Class, None] = Class.query.filter_by(uid=uid).first()

    if class_:
        return Response(
            json.dumps(class_.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Class with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/class/<string:uid>")
@login_required
def fetch_class(uid: str) -> Response:
    class_: Union[Class, None] = Class.query.filter_by(uid=uid).first()

    if class_:
        return Response(
            json.dumps(class_.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Class with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/class")
@login_required
def add_class() -> Response:
    form: AddClassForm = AddClassForm()

    response: Dict = {}

    if form.validate_on_submit():
        class_: Class = Class()

        class_.name = form.name.data
        class_.teacher_id = form.teacher_id.data

        db.session.add(class_)
        db.session.commit()

        response["message"] = "Class added successfully."
        response["title"] = "Added!"
        response["category"] = "success"
        response["id"] = class_.uid

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)


@bp.post("/update/class")
@login_required
def update_class() -> Response:
    form: UpdateClassForm = UpdateClassForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        class_: Union[Class, None] = Class.query.filter_by(uid=form.uid.data).first()

        if class_:
            class_.name = form.name.data
            class_.teacher_id = form.teacher_id.data

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Class updated successfully!",
                    "category": "success",
                }
            )

    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/class/<string:uid>")
@login_required
def delete_class(uid: str) -> Response:
    response: Dict = {}

    class_: Union[Class, None] = Class.query.filter_by(uid=uid).first()
    if class_:
        db.session.delete(class_)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Class deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Class not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
