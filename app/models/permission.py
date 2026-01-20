from typing import Any, Dict

from app.extensions import db


class Permission(db.Model):
    __tablename__ = "permissions"

    name = db.Column(db.String(64), unique=True)
    permission = db.Column(db.String(32))

    permissions: Dict[str, int] = {"ADMINISTER": 0xFFFF}

    @property
    def _permission(self):
        return eval(self.permission)

    @classmethod
    def get(cls, name: str) -> Any:
        cls.permissions.setdefault(name, 0x1 << len(cls.permissions))

        cls.permissions = dict(
            sorted(
                {
                    (
                        (
                            key,
                            max(cls.permissions.values())
                            << (
                                1
                                if value
                                <= max(
                                    list(
                                        {
                                            v
                                            for k, v in cls.permissions.items()
                                            if k != key
                                        }
                                        | {0x0}
                                    )
                                )
                                else 0
                            ),
                        )
                        if key == "ADMINISTER"
                        else (key, value)
                    )
                    for key, value in Permission.permissions.items()
                },
                key=lambda item: item.__getitem__(-1),
            )
        )

        return (permission := cls.permissions.get(name, 0x0)) << (
            1
            if name == "ADMINISTER"
            and permission
            <= max(
                {value for key, value in cls.permissions.items() if key != name} | {0x0}
            )
            else 0
        )

    @classmethod
    def administer(cls):
        return cls.get("ADMINISTER")

    @staticmethod
    def insert_permissions():
        for name in Permission.permissions.keys():
            p: Permission = Permission()

            p.name = name
            p.permission = hex(Permission.get(name))

            db.session.add(p)
            db.session.commit()
