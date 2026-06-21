import subprocess
import tempfile
from tempfile import NamedTemporaryFile

from docxtpl import DocxTemplate
from flask import send_file

from app.blueprints.api import bp
from app.models.student import Student


@bp.get("/export/student/<string:uid>/registration-form")
def export_student_registration_form(uid: str):
    student = Student.query.filter_by(uid=uid).first_or_404()

    doc = DocxTemplate("app/templates/docx/student-registration-form.docx")

    context = {
        key.replace("-", "_"): str(value) if value is not None else ""
        for key, value in student.to_dict().items()
    }

    doc.render(context)

    tmp = NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    tmp.close()

    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            tempfile.gettempdir(),
            tmp.name,
        ],
        check=True,
    )

    pdf_path = tmp.name.replace(".docx", ".pdf")

    return send_file(
        pdf_path,
        download_name=f"student_registration_{student.uid}.pdf",
        mimetype="application/pdf",
    )
