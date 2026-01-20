from typing import Any, Dict, Tuple

from app.extensions import db
from app.models.permission import Permission


class Role(db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.String(25))

    users = db.relationship("User", back_populates="role")

    roles: Dict[str, Tuple[int, bool]] = {
        "ANONYMOUS": (0x0000, True),
        "ADMINISTRATOR": (0xFFFF, False),
    }

    default = (0x0000, False)

    @property
    def _permissions(self) -> int:
        return eval(self.permissions)

    @classmethod
    def get(cls, name: str) -> Any:
        role = cls.query.filter_by(name=name).scalar()

        if not role:
            role = cls()

        role.name = name
        permissions, default = cls.default
        role.permissions, role.default = hex(permissions), default

        db.session.add(role)
        db.session.commit()

        return role

    @classmethod
    def administrator(cls):
        permissions = 1

        for permission in Permission.permissions.values():
            permissions |= permission

        cls.roles.__setitem__("ADMINISTRATOR", (permissions, False))

        return permissions

    @classmethod
    def insert(cls):
        if cls.administrator():
            for name, (permissions, default) in cls.roles.items():
                role = Role.query.filter_by(name=name).first()

                if role is None:
                    role = Role()

                role.name = name
                role.permissions, role.default = hex(permissions), default or False

                db.session.add(role)
                db.session.commit()
