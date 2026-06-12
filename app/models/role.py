from operator import call
from typing import Any, List

from app.const import ADMINISTRATOR
from app.extensions.db import db
from app.models.permission import Permission


class Role(db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(2500), nullable=True)
    default = db.Column(db.Boolean, default=False, index=True)
    primary = db.Column(db.Boolean, default=True)

    permissions = db.relationship(
        "Permission",
        secondary="roles_permissions",
        backref=db.backref("roles", lazy="dynamic"),
        lazy="dynamic",
    )
    user = db.relationship("User")

    @property
    def hex_permissions(self) -> int:
        permissions = 0x0000

        for p in self.permissions.all():
            permissions |= p.hex_permission

        return permissions

    @classmethod
    def get(cls, name: str, primary: bool = False) -> Any:
        role = cls.query.filter_by(name=name).scalar()

        if not role:
            role = cls()

            role.name = name
            role.primary = primary

            db.session.add(role)

        role.primary = primary

        db.session.commit()

        return role

    @classmethod
    def administrator(cls):
        return cls.get(name=ADMINISTRATOR, primary=True)

    def to_dict(self) -> dict:
        readonly: List[str] = ["name"]

        if self == self.administrator():
            readonly.extend(["permissions", "default"])

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
