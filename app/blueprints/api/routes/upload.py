import json
import os
import re
import uuid
from datetime import datetime as dt
from typing import Dict, List

from flask import Response, current_app, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.file import File
from app.models.permission import Permission
from app.models.user import permission_required

from .. import bp


@bp.post("/upload")
@login_required
@permission_required(Permission.get("UPLOAD_FILE"))
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
            else str(".txt")
        )

        filename = f"{uuid.uuid4()}{ext}"

        file.save(
            os.path.join(
                dst,
                secure_filename(filename),
            )
        )

        file = File()
        file.user_id = current_user.uid
        file.file_name = request.form.get("filename", filename)
        file.file_description = request.form.get("file_description")
        file.file_for = request.form.get("file_for")
        file.file_url = url_for("static", filename=f"uploads/{today}/{filename}")

        db.session.add(file)
        db.session.commit()

        lst.append(
            {
                "message": "File successfully uploaded.",
                "category": "success",
                "file": file.to_dict(),
                "status": 200,
            }
        )

    response.response = json.dumps(lst)

    return response
