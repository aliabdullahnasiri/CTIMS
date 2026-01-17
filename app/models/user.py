import enum
from datetime import date
from functools import wraps
from typing import Dict, List, Union

from flask import abort, current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin, current_user

from app.constants import DEFAULT_AVATAR
from app.extensions import bcrypt, db, login_manager
from app.functions import get_file_url


@enum.unique
class PermissionEnum(enum.Enum):
    CREATE_USER = 0x0000001
    UPDATE_USER = 0x0000002
    DELETE_USER = 0x0000004
    FETCH_USER = 0x0000008
    FETCH_USERS = 0x0000010

    ADMINISTER = 0x8000000


class RoleEnum(enum.Enum):
    ANONYMOUS = 0x0000000, True
    EMPLOYEE = 0x0000000, False
    TEACHER = 0x0000000, False
    STUDENT = 0x0000000, False
    ADMINISTRATOR = 0xFFFFFFF, False


class Role(db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship("User", back_populates="role")

    @staticmethod
    def insert_roles():
        try:
            for r in sorted(
                [
                    e
                    for attr in dir(RoleEnum)
                    if attr.isupper() and type(e := getattr(RoleEnum, attr)) == RoleEnum
                ],
                key=lambda role: role.value.__getitem__(0),
            ):
                role = Role.query.filter_by(name=r.name).first()

                if role is None:
                    role = Role()

                role.name = r.name
                role.permissions, role.default = r.value

                db.session.add(role)
                db.session.commit()

        except Exception as err:
            print(f"ERROR: {err}")


class User(UserMixin, db.Model):
    __tablename__ = "users"

    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(128), nullable=False)

    birthday = db.Column(db.Date)
    role_uid = db.Column(db.String(8), db.ForeignKey("roles.uid"))

    avatar_path = db.Column(
        db.String(255),
        nullable=True,
    )

    employee = db.relationship("Employee", back_populates="user", cascade="delete")
    role = db.relationship("Role", back_populates="users")

    def __init__(self) -> None:
        super().__init__()

        if self.role is None:
            if self.email == current_app.config["FLASKY_ADMIN"]:
                self.role = Role.query.filter_by(
                    permissions=RoleEnum.ADMINISTRATOR.value
                ).first()

            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return (
            self.role is not None
            and (self.role.permissions & permissions) == permissions
        )

    def is_administrator(self):
        return self.can(PermissionEnum.ADMINISTER.value)

    def to_dict(self) -> Dict:
        dct = {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "full_name": self.full_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_src,
            **super().to_dict(),
        }

        return dct

    def get_id(self):
        return str(self.uid)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_name}>"

    @property
    def full_name(self) -> str:
        """Return full name with middle name if exists."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name or 'N/A'} {self.last_name or 'N/A'}"

    @property
    def age(self) -> int | None:
        if self.birthday is None:
            return None
        today = date.today()
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    @property
    def display_birthday(self):
        if self.birthday:
            return self.birthday.strftime("%Y-%m-%d")

        return "N/A"

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)

    def update_files(self, files: Dict[str, Union[str, List[str]]]) -> None:
        for key, value in files.items():
            match key:
                case "avatar" if type(value) == str:
                    self.avatar_path = get_file_url(value)
                    db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(uid: str):
    return User.query.filter_by(uid=uid).first()


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(PermissionEnum.ADMINISTER.value)(f)
