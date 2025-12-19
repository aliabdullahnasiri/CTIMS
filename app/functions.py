import pathlib

from flask import render_template

from app.config import Config
from app.extensions import console


def render_td(col_id: str, obj) -> str:
    dct = obj.to_dict()

    for TEMP in Config.TD_TEMPS:
        if col_id.lstrip("temp_") == TEMP.name.split(chr(46)).pop(0):
            try:
                return render_template(
                    f"admin/components/tables/td/{TEMP.name}",
                    **{col_id.lstrip("temp_"): getattr(obj, col_id.lstrip("temp_"))},
                )
            except AttributeError as _:
                pass

            return render_template(f"admin/components/tables/td/{TEMP.name}", **dct)

    return dct.get(col_id, "N/A")
