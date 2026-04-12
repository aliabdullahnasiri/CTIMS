from decimal import Decimal
from operator import call
from typing import Dict

from numerize.numerize import numerize
from sqlalchemy import func

from app.const import CURRENCY_SYMBOL
from app.extensions.db import db
from app.models.employee import Employee


class Job(db.Model):
    __tablename__ = "jobs"

    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    min_salary = db.Column(db.Numeric(12, 2), nullable=False)
    max_salary = db.Column(db.Numeric(12, 2), nullable=False)

    employees = db.relationship(
        "Employee",
        back_populates="job",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Job title={self.job_title!r}>"

    def to_dict(self) -> Dict:
        dct = {
            "job_title": self.job_title,
            "job_description": self.job_description,
            "min_salary": float(self.min_salary) if self.min_salary else None,
            "max_salary": float(self.max_salary) if self.max_salary else None,
            **call(getattr(super(), "to_dict")),
        }

        return dct

    @property
    def employee_count(self) -> int:
        return self.employees.count()

    @property
    def average_salary(self) -> float | None:
        return (
            db.session.query(func.avg(Employee.salary).label("a"))
            .filter(Employee.job_uid == getattr(self, "uid"))
            .scalar()
        )

    @property
    def highest_salary(self) -> float | None:
        return (
            db.session.query(func.max(Employee.salary).label("a"))
            .filter(Employee.job_uid == getattr(self, "uid"))
            .scalar()
        )

    @property
    def lowest_salary(self) -> float | None:
        return (
            db.session.query(func.min(Employee.salary).label("a"))
            .filter(Employee.job_uid == getattr(self, "uid"))
            .scalar()
        )

    @property
    def display_min_salary(self) -> str:
        if type(self.min_salary) is Decimal:
            return f"{CURRENCY_SYMBOL}{self.min_salary:.2f}"

        return "N/A"

    @property
    def display_max_salary(self) -> str:
        if type(self.max_salary) is Decimal:
            return f"{CURRENCY_SYMBOL}{self.max_salary:.2f}"

        return "N/A"

    @property
    def display_salary_range(self) -> str:
        if self.min_salary and self.max_salary:
            return f"{CURRENCY_SYMBOL}{self.min_salary:,.2f} - {CURRENCY_SYMBOL}{self.max_salary:,.2f}"
        elif self.min_salary:
            return f"{CURRENCY_SYMBOL}{self.min_salary:,.2f} and up"
        elif self.max_salary:
            return f"Up to {CURRENCY_SYMBOL}{self.max_salary:,.2f}"
        return "N/A"

    @property
    def display_average_salary(self) -> str:
        if self.average_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.average_salary:,.2f}"

    @property
    def display_highest_salary(self) -> str:
        if self.highest_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.highest_salary:,.2f}"

    @property
    def display_lowest_salary(self) -> str:
        if self.lowest_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.lowest_salary:,.2f}"

    @property
    def display_title(self) -> str:
        return self.job_title or "N/A"

    @property
    def display_description(self) -> str:
        return self.job_description or "No description"

    @property
    def display_employee_count(self) -> str:
        return numerize(self.employee_count)
