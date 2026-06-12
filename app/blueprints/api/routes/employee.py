import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_babel import gettext as g

from app.blueprints.api import bp
from app.cls import ColumnID, ColumnName
from app.const import DEFAULT_AVATAR, EMPLOYEE
from app.extensions.console import console
from app.extensions.db import db
from app.forms.employee import AddEmployeeForm, UpdateEmployeeForm
from app.func import render_td
from app.models.employee import Employee
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User, permission_required

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName(g("UID"))),
    (ColumnID("temp_employee"), ColumnName(g("Employee"))),
    (ColumnID("birthday"), ColumnName(g("Birthday"))),
    (ColumnID("age"), ColumnName(g("Age"))),
    (ColumnID("hire_date"), ColumnName(g("Hire Date"))),
    (ColumnID("salary"), ColumnName(g("Salary"))),
]


@bp.get("/fetch/employees")
@permission_required(Permission.get("FETCH_EMPLOYEES"))
def fetch_employees() -> Response:
    employees: List[Dict] = [employee.to_dict() for employee in Employee.query.all()]

    return Response(
        json.dumps(employees),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/rows/employees")
@permission_required(Permission.get("FETCH_EMPLOYEES"))
def fetch_employees_rows() -> Response:
    employees: List[Employee] = Employee.query.all()

    rows: List[List] = []

    for employee in employees:
        row = [render_td(col_id, employee) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": [(col_id, g(col_name)) for col_id, col_name in cols],
        "rows": rows,
    }

    return Response(
        json.dumps(dct),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/row/employee/<string:uid>")
@permission_required(Permission.get("FETCH_EMPLOYEE"))
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
                "message": g("Employee with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.get("/fetch/employee/<string:uid>")
@permission_required(Permission.get("FETCH_EMPLOYEE"))
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
                "message": g("Employee with the given ID was not found :("),
                "category": "error",
            }
        ),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/employee")
@permission_required(Permission.get("CREATE_EMPLOYEE"))
def add_employee() -> Response:
    form: AddEmployeeForm = AddEmployeeForm()

    response: Dict = {}

    if form.validate_on_submit():
        user: User = User()

        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.birthday = form.birthday.data
        user.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        if form.password.data:
            user.set_password(form.password.data)

        db.session.add(user)

        if role := Role.get(EMPLOYEE):
            user.update_roles(primary_role=role)

        db.session.commit()

        employee: Employee = Employee()
        employee.user_uid = getattr(user, "uid")
        employee.address = form.address.data
        employee.salary = form.salary.data
        employee.job_uid = form.job_uid.data if form.job_uid.data else None

        db.session.add(employee)
        db.session.commit()

        if form.phones.data:
            employee.user.update_phones(json.loads(form.phones.data))

        if files := request.form.get("files"):
            try:
                employee.user.update_files(json.loads(files))
            except json.JSONDecodeError as err:
                console.print(err)

        db.session.commit()

        response["message"] = g("Employee added successfully.")
        response["title"] = g("Added!")
        response["category"] = "success"
        response["id"] = getattr(employee, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)


@bp.post("/update/employee")
@permission_required(
    Permission.get("UPDATE_EMPLOYEE") | Permission.get("FETCH_EMPLOYEE")
)
def update_employee() -> Response:
    form: UpdateEmployeeForm = UpdateEmployeeForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        employee: Union[Employee, None] = Employee.query.filter_by(
            uid=form.uid.data
        ).first()

        if employee:
            employee.user.first_name = form.first_name.data
            employee.user.middle_name = form.middle_name.data
            employee.user.last_name = form.last_name.data
            employee.user.email = form.email.data
            employee.user.birthday = form.birthday.data
            employee.address = form.address.data
            employee.salary = form.salary.data

            if form.job_uid.data:
                employee.job_uid = form.job_uid.data

            if form.password.data:
                employee.user.set_password(form.password.data)

            if form.phones.data:
                employee.user.update_phones(json.loads(form.phones.data))

            if files := request.form.get("files"):
                try:
                    employee.user.update_files(json.loads(files))
                except json.JSONDecodeError as err:
                    console.print(err)

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": g("Good job!"),
                    "message": g("Employee updated successfully!"),
                    "category": "success",
                }
            )

    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/employee/<string:uid>")
@permission_required(
    Permission.get("DELETE_EMPLOYEE") | Permission.get("FETCH_EMPLOYEE")
)
def delete_employee(uid: str) -> Response:
    response: Dict = {}

    employee: Union[Employee, None] = Employee.query.filter_by(uid=uid).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()

        response["title"] = g("Deleted!")
        response["message"] = g("Employee deleted successfully")
        response["category"] = "success"
        response["status"] = 200
    else:
        response["title"] = g("Error :(")
        response["message"] = g("Employee not found")
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )
