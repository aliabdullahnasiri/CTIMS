import re

from flask import render_template

from app.config import Config


def validate_uid(uid: str) -> bool:
    return bool(re.match(Config.UID_PATTERN, uid))


def render_td(col_id: str, obj) -> str:
    dct = obj.to_dict()

    for TEMP in Config.TD_TEMPS:
        if col_id.startswith(let := "temp_"):
            col_id = col_id[len(let) :]

        if col_id == TEMP.name.split(chr(46)).pop(0):
            try:
                return render_template(
                    f"admin/components/tables/td/{TEMP.name}",
                    **{col_id: getattr(obj, col_id)},
                )
            except AttributeError as _:
                pass

            return render_template(f"admin/components/tables/td/{TEMP.name}", **dct)

    if hasattr(obj, attr := f"display_{col_id}"):
        return getattr(obj, attr)

    return dct.get(col_id, "N/A")
