from datetime import datetime
from typing import Any, Literal

import humanize
from flask import request
from numerize import numerize
from sqlalchemy import Column, Integer, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions.console import console
from app.extensions.db import db


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True, index=True)

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

    @hybrid_property
    def uid(self):
        return f"U-{self.id:08d}"

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
