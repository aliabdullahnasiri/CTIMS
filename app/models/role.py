from operator import call
from typing import Any, List

from flask import current_app

from app.constants import ADMINISTRATOR
from app.extensions.db import db
from app.models.permission import Permission


class Role(db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(2500), nullable=True)
    default = db.Column(db.Boolean, default=False, index=True)

    permissions = db.relationship(
        "Permission",
        secondary="roles_permissions",
        backref=db.backref("roles", lazy="dynamic"),
        lazy="dynamic",
    )

    @property
    def hex_permissions(self) -> int:
        permissions = 0x0001

        for permission in (
            Permission.permissions.values()
            if self.name == ADMINISTRATOR
            else [p.hex_permission for p in self.permissions.all()]
        ):
            permissions |= permission

        return permissions

    @classmethod
    def get(cls, name: str) -> Any:
        role = cls.query.filter_by(name=name).scalar()

        if not role:
            role = cls()

            role.name = name

            db.session.add(role)
            db.session.commit()

        return role

    @classmethod
    def administrator(cls):
        return cls.get(name=ADMINISTRATOR)

    def to_dict(self) -> dict:
        readonly: List[str] = ["name"]

        if self == self.administrator():
            readonly.append("permissions")
            readonly.append("default")

        return {
            "name": self.name,
            "description": self.description,
            "default": self.default,
            "permissions": [
                p.uid
                for p in (
                    Permission.query.all()
                    if self.name == ADMINISTRATOR
                    else self.permissions.all()
                )
            ],
            "readonly": readonly,
            **call(getattr(super(), "to_dict")),
        }
