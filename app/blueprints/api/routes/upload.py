import json
import os
import re
import uuid
from datetime import datetime as dt
from typing import Dict, List

from flask import Response, current_app, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from .. import bp


@bp.post("/upload")
@login_required
def upload() -> Response:
    response: Response = Response(headers={"Content-Type": "application/app"})

    lst: List[Dict] = []

    for file in request.files.values():
        dst = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            today := dt.now().strftime("%Y-%m-%d"),
        )

        os.makedirs(dst, exist_ok=True)

        ext = (
            lst.pop()
            if len(lst := re.findall(r".[a-zA-Z]{1,}$", f"{file.filename}")) > 0
            else str()
        )

        if not ext:
            lst.append(
                {
                    "message": "File doesn't have extension, yet!",
                    "category": "error",
                    "status": 500,
                }
            )

            continue

        filename = f"{uuid.uuid4()}{ext}"

        file.save(
            os.path.join(
                dst,
                secure_filename(filename),
            )
        )

        lst.append(
            {
                "message": "File successfully uploaded.",
                "category": "success",
                "file": {
                    "name": file.filename,
                    "url": url_for("static", filename=f"uploads/{today}/{filename}"),
                },
                "status": 200,
            }
        )

    response.response = json.dumps(lst)

    return response
