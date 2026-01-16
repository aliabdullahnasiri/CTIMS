from datetime import datetime, timezone
from typing import Any, Dict, List, Union

from flask import url_for
from numerize.numerize import numerize

from app.constants import CURRENCY_SYMBOL, DEFAULT_AVATAR
from app.extensions import db
from app.functions import get_file_url
from app.models.phone import EmployeePhone


class Employee(db.Model):
    __tablename__ = "employees"

    # Foreign Keys
    job_uid = db.Column(db.String(8), db.ForeignKey("jobs.uid"), nullable=True)
    user_uid = db.Column(db.String(8), db.ForeignKey("users.uid"), nullable=False)

    # Employment Info
    address = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.Numeric(12, 2), nullable=True)
    hire_date = db.Column(
        db.Date, nullable=False, default=datetime.now(timezone.utc).date
    )

    # Relationships
    job = db.relationship("Job", back_populates="employees")
    user = db.relationship("User", back_populates="employee")
    phones = db.relationship(
        "EmployeePhone", back_populates="employee", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Employee {self.user.first_name} {self.user.last_name} ID={self.uid}>"

    def to_dict(self):
        dct = {
            "employee_uid": self.uid,
            "job_uid": self.job_uid,
            "first_name": self.user.first_name,
            "middle_name": self.user.middle_name,
            "last_name": self.user.last_name,
            "full_name": self.user.full_name,
            "user_name": self.user.user_name,
            "email": self.user.email,
            "birthday": self.user.display_birthday,
            "age": self.user.age,
            "avatar": self.user.avatar_path,
            "address": self.address,
            "salary": f"{self.salary:.2f}" if self.salary is not None else None,
            "display_salary": self.display_salary,
            "hire_date": self.display_hire_date,
            "phones": [phone.phone_number for phone in self.phones],
            **super().to_dict(),
        }

        return dct

    @property
    def is_salary_gt_avg(self) -> bool:
        employees = self.query.all()
        lst = [employee.salary.__int__() for employee in employees]
        average_salary = sum(lst) / len(lst)

        return self.salary > average_salary

    @property
    def display_salary(self) -> str:
        """Display salary with currency symbol."""
        if self.salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{float(self.salary):,.2f}"

    @property
    def display_hire_date(self) -> str:
        return self.hire_date.strftime("%Y-%m-%d") if self.hire_date else "N/A"

    @property
    def display_address(self) -> str:
        return self.address or "N/A"

    @property
    def avatar_src(self) -> str:
        if self.user.avatar_path:
            return self.user.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)

    @property
    def display_number_of_phone_nums(self):
        return numerize(len(self.phones), decimals=2)

    def update_phones(self, phones: List[str]):
        for phone in self.phones:
            if phone.phone_number not in phones:
                db.session.delete(phone)

        db.session.commit()

        for p in phones:
            if EmployeePhone.query.filter_by(
                employee_id=self.uid, phone_number=p
            ).first():
                continue

            phone = EmployeePhone()
            phone.employee_id = self.uid
            phone.phone_number = p

            db.session.add(phone)

        db.session.commit()

    def update_files(self, files: Dict[str, Union[str, List[str]]]) -> None:
        for key, value in files.items():
            match key:
                case "avatar" if type(value) == str:
                    self.user.avatar_path = get_file_url(value)
                    db.session.commit()
