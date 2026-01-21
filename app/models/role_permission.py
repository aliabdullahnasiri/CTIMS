from sqlalchemy import UniqueConstraint

from app.extensions import db


class RolePermission(db.Model):
    __tablename__ = "roles_permissions"

    role_uid = db.Column(db.String(8), db.ForeignKey("roles.uid"), nullable=False)
    permission_uid = db.Column(
        db.String(8), db.ForeignKey("permissions.uid"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("role_uid", "permission_uid", name="uix_role_permission"),
    )

    def to_dict(self) -> dict:
        return {
            "role_uid": self.role_uid,
            "permission_uid": self.permission_uid,
            **super().to_dict(),
        }

    def __repr__(self):
        return f"<RolePermission role_uid='{self.role_uid}' permission_uid='{self.permission_uid}'>"
