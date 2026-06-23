import hashlib
import os
import subprocess
import uuid
from datetime import datetime as dt
from operator import call
from tempfile import NamedTemporaryFile

from docxtpl import DocxTemplate
from flask import current_app, send_file
from sqlalchemy import and_

from app.blueprints.api import bp
from app.extensions.db import db
from app.models.form import Form, FormType
from app.models.student import Student


@bp.get("/export/student/<string:uid>/registration-form")
def export_student_registration_form(uid: str):
    student = Student.query.filter_by(uid=uid).first_or_404()

    if not (
        (
            form := student.forms.filter(
                Form._type == FormType.STUDENT_REGISTRATION_FORM
            )
            .order_by(getattr(Form, "id").desc())
            .first()
        )
        and form._hash
        == hashlib.sha256(
            student.updated_at.strftime("%Y-%m-%d %H:%M:%S.%f").encode("UTF-8")
        ).hexdigest()
    ):
        path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            dt.now().strftime("%Y-%m-%d"),
        )

        os.makedirs(path, exist_ok=True)

        form: Form = Form()

        form.name = "Student Registration Form"
        form._type = FormType.STUDENT_REGISTRATION_FORM
        form._hash = hashlib.sha256(
            student.updated_at.strftime("%Y-%m-%d %H:%M:%S.%f").encode("UTF-8")
        ).hexdigest()

        form.students.add(student)
        db.session.flush()

        student.forms.add(form)

        doc = DocxTemplate("app/templates/docx/student-registration-form.docx")

        doc.render(
            {
                key.replace("-", "_"): str(value) if value is not None else ""
                for key, value in (
                    student.to_dict()
                    | {
                        "form_number": getattr(form, "id"),
                        "distribution_date": getattr(form, "display_distribution_date"),
                        "academic_year": (
                            student.daily_section.academic_year
                            if student.daily_section
                            else ""
                        ),
                    }
                ).items()
            }
        )

        doc.save(_f := os.path.join(path, filename := f"{uuid.uuid4()}.docx"))

        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                path,
                _f,
            ],
            check=True,
        )

        form._path = os.path.join(path, filename.replace(".docx", ".pdf")).replace(
            "app/", ""
        )

        db.session.commit()

    return send_file(
        form._path,
        download_name=f"student_registration_{student.uid}.pdf",
        mimetype="application/pdf",
    )
