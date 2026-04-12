from operator import call

from sqlalchemy import UniqueConstraint

from app.extensions.db import db


class UserRole(db.Model):
    __tablename__ = "users_roles"

    role_uid = db.Column(db.String(8), db.ForeignKey("roles.uid"), nullable=False)
    user_uid = db.Column(db.String(8), db.ForeignKey("users.uid"), nullable=False)

    __table_args__ = (UniqueConstraint("role_uid", "user_uid", name="uix_role_user"),)

    def to_dict(self) -> dict:
        return {
            "role_uid": self.role_uid,
            "user_uid": self.user_uid,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<UserRole role_uid='{self.role_uid}' user_uid='{self.user_uid}'>"
