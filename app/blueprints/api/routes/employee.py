import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms.employee import AddEmployeeForm, UpdateEmployeeForm
from app.functions import render_td
from app.models.employee import Employee
from app.models.phone import EmployeePhone
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_employee"), ColumnName("Employee")),
    (ColumnID("birthday"), ColumnName("Birthday")),
    (ColumnID("age"), ColumnName("Age")),
    (ColumnID("hire_date"), ColumnName("Hire Date")),
    (ColumnID("salary"), ColumnName("Salary")),
]


@bp.get("/fetch/employees")
@login_required
def fetch_employees() -> Response:
    employees: List[Dict] = [employee.to_dict() for employee in Employee.query.all()]

    return Response(
        json.dumps(employees),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/employees")
@login_required
def fetch_employees_rows() -> Response:
    employees: List[Employee] = Employee.query.all()

    rows: List[List] = []

    for employee in employees:
        row = [render_td(col_id, employee) for col_id, _ in cols]
        rows.append(row)

    return Response(
        json.dumps({"cols": cols, "rows": rows}),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/employee/<string:uid>")
@login_required
def fetch_employee_row(uid: str) -> Response:
    employee: Union[Employee, None] = Employee.query.filter_by(uid=uid).first()

    if employee:
        return Response(
            json.dumps(
                {
                    key: val
                    for key, val in zip(
                        [col_id for col_id, _ in cols],
                        [render_td(col_id, employee) for col_id, _ in cols],
                    )
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Employee with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/employee/<string:uid>")
@login_required
def fetch_employee(uid: str) -> Response:
    employee: Union[Employee, None] = Employee.query.filter_by(uid=uid).first()

    if employee:
        return Response(
            json.dumps(employee.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return Response(
        json.dumps(
            {
                "message": "Employee with the given ID was not found :(",
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/employee")
@login_required
def add_employee() -> Response:
    form: AddEmployeeForm = AddEmployeeForm()

    response: Dict = {}

    if form.validate_on_submit():
        employee: Employee = Employee()

        employee.first_name = form.first_name.data
        employee.middle_name = form.middle_name.data
        employee.last_name = form.last_name.data

        if form.email.data:
            employee.email = form.email.data

        employee.birthday = form.birthday.data
        employee.address = form.address.data
        employee.salary = form.salary.data

        if form.job_id.data:
            employee.job_id = form.job_id.data

        employee.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        try:
            links = json.loads(request.form.get("links", "{}"))

            if type(links) == dict:
                for key, value in links.items():
                    match key:
                        case "avatar":
                            if value:
                                employee.avatar_path = value

        except Exception as err:
            console.print(err)

        db.session.add(employee)
        db.session.commit()

        if form.phones.data:
            try:
                for phone in json.loads(form.phones.data):
                    if EmployeePhone.query.filter_by(phone_number=phone).first():
                        continue

                    employee_phone = EmployeePhone()
                    employee_phone.employee_id = employee.uid
                    employee_phone.phone_number = phone

                    db.session.add(employee_phone)

                db.session.commit()
            except Exception as err:
                console.print(err)

        response["message"] = "Employee added successfully."
        response["title"] = "Added!"
        response["category"] = "success"
        response["id"] = employee.uid

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)


@bp.post("/update/employee")
@login_required
def update_employee() -> Response:
    form: UpdateEmployeeForm = UpdateEmployeeForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        employee: Union[Employee, None] = Employee.query.filter_by(
            uid=form.uid.data
        ).first()

        if employee:
            employee.first_name = form.first_name.data
            employee.middle_name = form.middle_name.data
            employee.last_name = form.last_name.data
            employee.email = form.email.data
            employee.birthday = form.birthday.data
            employee.address = form.address.data
            employee.salary = form.salary.data

            if form.job_id.data:
                employee.job_id = form.job_id.data

            db.session.commit()

            if form.phones.data:
                employee.update_phones(json.loads(form.phones.data))

            if files := request.form.get("files"):
                try:
                    employee.update_files(json.loads(files))
                except json.JSONDecodeError as err:
                    console.print(err)

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Employee updated successfully!",
                    "category": "success",
                }
            )

    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/employee/<string:uid>")
@login_required
def delete_employee(uid: str) -> Response:
    response: Dict = {}

    employee: Union[Employee, None] = Employee.query.filter_by(uid=uid).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Employee deleted successfully"
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = "Error :("
        response["message"] = "Employee not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
