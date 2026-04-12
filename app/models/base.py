from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import humanize
from flask import request
from numerize import numerize
from sqlalchemy import Column, Integer, String, event, extract, func
from sqlalchemy.ext.declarative import declared_attr

from app.extensions.console import console
from app.extensions.db import db


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True, index=True)

    @declared_attr
    def uid(cls):
        return Column(String(8), primary_key=False, unique=True)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )

    @classmethod
    def yearly_growth(cls):
        current_year = datetime.now().year
        last_year = current_year - 1

        current_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("year", cls.created_at) == current_year)
            .scalar()
        )

        previous_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("year", cls.created_at) == last_year)
            .scalar()
        )

        return cls._percent_change(current_count, previous_count)

    @classmethod
    def yearly_growth_clr(cls):
        if cls.yearly_growth() > 0:
            return "success"

        return "danger"

    @classmethod
    def yearly_growth_icon(cls):
        if cls.yearly_growth() > 0:
            return "arrow_upward"

        return "arrow_downward"

    @classmethod
    def display_yearly_growth(cls):
        sign = chr(43) if (g := cls.yearly_growth()) > 0 else chr(45)

        if g == 0:
            sign = str()

        return f"{sign}{abs(g)}{chr(37)}"

    @classmethod
    def weekly_growth(cls):
        now = datetime.now(timezone.utc)

        start_of_week = datetime.combine(
            (now - timedelta(days=now.weekday())).date(),
            datetime.min.time(),
            tzinfo=timezone.utc,
        )
        start_of_last_week = start_of_week - timedelta(weeks=1)
        end_of_last_week = start_of_week

        current_week = (
            db.session.query(cls).filter(cls.created_at >= start_of_week).count()
        )

        previous_week = (
            db.session.query(cls)
            .filter(
                cls.created_at >= start_of_last_week, cls.created_at < end_of_last_week
            )
            .count()
        )

        return cls._percent_change(current_week, previous_week)

    @classmethod
    def weekly_growth_clr(cls):
        if cls.weekly_growth() > 0:
            return "success"

        return "danger"

    @classmethod
    def display_weekly_growth(cls):
        sign = chr(43) if (g := cls.weekly_growth()) > 0 else chr(45)

        if g == 0:
            sign = str()

        return f"{sign}{abs(g)}{chr(37)}"

    @classmethod
    def weekly_growth_icon(cls):
        if cls.weekly_growth() > 0:
            return "arrow_upward"

        return "arrow_downward"

    @classmethod
    def monthly_growth(cls):
        current_month = datetime.now().month
        last_month = current_month - 1 if current_month > 1 else 12

        current_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("month", cls.created_at) == current_month)
            .scalar()
        )

        previous_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("month", cls.created_at) == last_month)
            .scalar()
        )

        return cls._percent_change(current_count, previous_count)

    @classmethod
    def monthly_growth_clr(cls):
        if cls.monthly_growth() > 0:
            return "success"

        return "danger"

    @classmethod
    def display_monthly_growth(cls):
        sign = chr(43) if cls.monthly_growth() >= 0 else chr(45)
        growth = f"{sign}{abs(cls.monthly_growth())}{chr(37)}"

        return growth

    @staticmethod
    def _percent_change(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 2)

    @classmethod
    def count(cls):
        return numerize.numerize(cls.query.count(), 2)

    @property
    def display_created_at(self) -> str:
        return (
            self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "N/A"
        )

    @property
    def display_updated_at(self) -> str:
        return (
            self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else "N/A"
        )

    @property
    def display_natural_created_at(self) -> str:
        return humanize.naturaltime(self.updated_at)

    @property
    def display_natural_updated_at(self) -> str:
        return humanize.naturaltime(self.updated_at)

    def display_date(self, attr, ret_none: Literal[1, 0] = 0, format: str = "%Y-%m-%d"):
        if hasattr(self, attr):
            if date := getattr(self, attr):
                return date.strftime(format)

        return None if ret_none else "N/A"

    def to_dict(self):
        return {
            "id": self.id,
            "uid": getattr(self, "uid") if hasattr(self, "uid") else None,
            "natural_created_at": self.display_natural_created_at,
            "natural_updated_at": self.display_natural_updated_at,
            "created_at": self.display_created_at,
            "updated_at": self.display_updated_at,
        }

    def __setattr__(self, name: str, value: Any, /) -> None:
        if type(value) is str and not value:
            value = None

        return super().__setattr__(name, value)


@event.listens_for(Base, "before_insert", propagate=True)
def before_insert(mapper, connection, target) -> None: ...


@event.listens_for(Base, "after_insert", propagate=True)
def after_insert(mapper, connection, target) -> None: ...


@event.listens_for(Base, "before_insert", propagate=True)
def generate_uid(mapper, connection, target):
    cls = target.__class__
    obj = cls.query.order_by(cls.id.desc()).first()
    prefix = target.__class__.__name__[0].upper()
    val = "{}-{:>06}".format(prefix, (obj.id if obj else 0) + 1)
    target.uid = val if not len(val) > 8 else None


def all(self):
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))
        offset = (page - 1) * limit

        return self.offset(offset).limit(abs(limit))
    except Exception as err:
        console.print(err)

    return self


db.Model.query_class.all = all
db.Model = Base
