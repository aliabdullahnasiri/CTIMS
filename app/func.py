import pathlib
import re


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
