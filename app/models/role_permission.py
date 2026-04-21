from operator import call

from sqlalchemy import UniqueConstraint

from app.extensions.db import db


class RolePermission(db.Model):
    __tablename__ = "roles_permissions"

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uix_role_permission"),
    )

    def to_dict(self) -> dict:
        return {
            "role_id": self.role_id,
            "permission_id": self.permission_id,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<RolePermission role_id='{self.role_id!r}' permission_id='{self.permission_id!r}'>"
