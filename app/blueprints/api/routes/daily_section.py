import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.extensions.db import db
from app.forms.daily_section import AddDailySectionForm, UpdateDailySectionForm
from app.func import render_td
from app.models.daily_section import DailySection
from app.models.permission import Permission
from app.models.user import permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID_LABEL"))),
    (ColumnID("title"), ColumnName(g("TITLE_LABEL"))),
    (ColumnID("description"), ColumnName(g("DESCRIPTION_LABEL"))),
    (ColumnID("exam_uid"), ColumnName(g("EXAM_UID_LABEL"))),
]


@bp.get("/fetch/daily_sections")
@permission_required(Permission.get("FETCH_DAILY_SECTIONS"))
def fetch_daily_sections() -> Response:
    daily_sections: List[Dict] = [
        daily_section.to_dict() for daily_section in DailySection.query.all()
    ]

    return Response(
        json.dumps(daily_sections),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/daily_sections")
@permission_required(Permission.get("FETCH_DAILY_SECTIONS"))
def fetch_daily_sections_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    daily_sections: List[DailySection] = DailySection.query.all()
    rows: List[List] = []

    for daily_section in daily_sections:
        row = [render_td(col_id, daily_section) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": [(col_id, g(col_name)) for col_id, col_name in cols],
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/daily_section/<string:uid>")
@permission_required(Permission.get("FETCH_DAILY_SECTION"))
def fetch_daily_section_row(uid: str) -> Response:
    daily_section: Union[DailySection, None] = DailySection.query.filter_by(
        uid=uid
    ).first()

    if daily_section:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, daily_section) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("DAILY_SECTION_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/daily_section/<string:uid>")
@permission_required(Permission.get("FETCH_DAILY_SECTION"))
def fetch_daily_section(uid: str) -> Response:
    daily_section: Union[DailySection, None] = DailySection.query.filter_by(
        uid=uid
    ).first()

    if daily_section:
        return Response(
            json.dumps(daily_section.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": g("DAILY_SECTION_WITH_THE_GIVEN_ID_WAS_NOT_FOUND_MSG"),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/update/daily_section")
@permission_required(Permission.get("UPDATE_DAILY_SECTION"))
def update_daily_section() -> Response:
    response: Dict = {}

    form = UpdateDailySectionForm()

    if form.validate_on_submit():
        uid = form.uid.data

        daily_section: Union[DailySection, None] = DailySection.query.filter_by(
            uid=uid
        ).first()

        if daily_section:
            daily_section.exam_uid = form.exam_uid.data
            daily_section.title = form.title.data
            daily_section.description = form.description.data
            daily_section.starting_base_number = form.starting_base_number.data
            daily_section.academic_year = form.academic_year.data

            db.session.commit()

            response["title"] = g("UPDATED_SUCCESS_MSG")
            response["message"] = g("DAILY_SECTION_UPDATED_SUCCESSFULLY_SUCCESS_MSG")
            response["category"] = "success"
        else:
            response["title"] = g("NOT_FOUND_LABEL")
            response["message"] = g("DAILY_SECTION_RECORD_NOT_FOUND_MSG")
            response["category"] = "error"
    else:
        response["errors"] = form.errors
        print(form.errors)

    return Response(
        json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.delete("/delete/daily_section/<string:uid>")
@permission_required(Permission.get("DELETE_DAILY_SECTION"))
def delete_daily_section(uid: str):
    response = {}

    if daily_section := DailySection.query.filter_by(uid=uid).scalar():
        db.session.delete(daily_section)
        db.session.commit()

        response["title"] = g("DELETED_SUCCESS_MSG")
        response["message"] = g(
            "DAILY_SECTION_HAS_BEEN_DELETED_SUCCESSFULLY_SUCCESS_MSG"
        )
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("ERROR_ERROR")
        response["message"] = g("DAILY_SECTION_NOT_FOUND_MSG")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/daily_section")
@permission_required(Permission.get("CREATE_DAILY_SECTION"))
def add_daily_section():
    form = AddDailySectionForm()

    response: Dict = {}

    if form.validate_on_submit():
        daily_section: DailySection = DailySection()

        daily_section.exam_uid = form.exam_uid.data
        daily_section.title = form.title.data
        daily_section.description = form.description.data
        daily_section.starting_base_number = form.starting_base_number.data
        daily_section.academic_year = form.academic_year.data

        db.session.add(daily_section)
        db.session.commit()

        response["message"] = g("DAILY_SECTION_ADDED_SUCCESSFULLY_SUCCESS_MSG")
        response["title"] = g("DAILY_SECTION_ADDED_LABEL")
        response["category"] = "success"
        response["id"] = getattr(daily_section, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
