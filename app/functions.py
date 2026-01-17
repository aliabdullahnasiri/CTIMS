import pathlib
import re
from typing import Union

from flask import render_template

from app.config import Config
from app.models.file import File


def validate_uid(uid: str) -> bool:
    return bool(re.match(Config.UID_PATTERN, uid))


def get_file(id: int) -> Union[File, None]:
    return File.query.filter_by(id=id).first()


def get_file_url(id: int) -> Union[str, None]:
    file = File.query.filter_by(id=id).first()

    if file:
        return file.file_url


def render_td(col_id: str, obj, max_length: int = 64) -> str:
    dct = obj.to_dict()

    dct.setdefault("obj_{}".format(obj.__class__.__name__.lower()), obj)

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

    val = dct.get(col_id, "N/A")

    if type(val) == str and len(val) > max_length:
        return "{}...".format(val[slice(max_length)])

    return val


def __import_all__(path: str) -> None:
    ext = ".py"
    for module in pathlib.Path(path).glob(f"*{ext}"):
        __import__(
            re.sub(
                re.compile(rf"{ext}$"),
                "",
                f"{path.replace(chr(47), chr(46))}{chr(46)}{module.name}",
            )
        )
