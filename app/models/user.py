import enum
from datetime import date
from functools import wraps
from typing import Dict, List, Union

from flask import abort, current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin, current_user
from sqlalchemy import event

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

    CREATE_TIME = 0x0000020
    UPDATE_TIME = 0x0000040
    DELETE_TIME = 0x0000080
    FETCH_TIME = 0x0000100
    FETCH_TIMES = 0x0000200

    CREATE_DEPARTMENT = 0x0000400
    UPDATE_DEPARTMENT = 0x0000800
    DELETE_DEPARTMENT = 0x0001000
    FETCH_DEPARTMENT = 0x0002000
    FETCH_DEPARTMENTS = 0x0004000

    CREATE_SEMESTER = 0x0008000
    UPDATE_SEMESTER = 0x0010000
    DELETE_SEMESTER = 0x0020000
    FETCH_SEMESTER = 0x0040000
    FETCH_SEMESTERS = 0x0080000

    CREATE_JOB = 0x0100000
    UPDATE_JOB = 0x0200000
    DELETE_JOB = 0x0400000
    FETCH_JOB = 0x0800000
    FETCH_JOBS = 0x1000000

    CREATE_EMPLOYEE = 0x2000000
    UPDATE_EMPLOYEE = 0x4000000
    DELETE_EMPLOYEE = 0x8000000
    FETCH_EMPLOYEE = 0x10000000
    FETCH_EMPLOYEES = 0x20000000

    CREATE_TEACHER = 0x40000000
    UPDATE_TEACHER = 0x80000000
    DELETE_TEACHER = 0x100000000
    FETCH_TEACHER = 0x200000000
    FETCH_TEACHERS = 0x400000000

    CREATE_SUBJECT = 0x800000000
    UPDATE_SUBJECT = 0x1000000000
    DELETE_SUBJECT = 0x2000000000
    FETCH_SUBJECT = 0x4000000000
    FETCH_SUBJECTS = 0x8000000000

    CREATE_CLASS = 0x10000000000
    UPDATE_CLASS = 0x20000000000
    DELETE_CLASS = 0x40000000000
    FETCH_CLASS = 0x80000000000
    FETCH_CLASSES = 0x100000000000

    CREATE_STUDENT = 0x200000000000
    UPDATE_STUDENT = 0x400000000000
    DELETE_STUDENT = 0x800000000000
    FETCH_STUDENT = 0x1000000000000
    FETCH_STUDENTS = 0x2000000000000

    CREATE_EXAM = 0x4000000000000
    UPDATE_EXAM = 0x8000000000000
    DELETE_EXAM = 0x10000000000000
    FETCH_EXAM = 0x20000000000000
    FETCH_EXAMS = 0x40000000000000

    CREATE_RESULT = 0x80000000000000
    UPDATE_RESULT = 0x100000000000000
    DELETE_RESULT = 0x200000000000000
    FETCH_RESULT = 0x400000000000000
    FETCH_RESULTS = 0x800000000000000

    CREATE_TEACHER_ATTENDANCE = 0x1000000000000000
    UPDATE_TEACHER_ATTENDANCE = 0x2000000000000000
    DELETE_TEACHER_ATTENDANCE = 0x4000000000000000
    FETCH_TEACHER_ATTENDANCE = 0x8000000000000000
    FETCH_TEACHER_ATTENDANCES = 0x10000000000000000

    CREATE_STUDENT_ATTENDANCE = 0x20000000000000000
    UPDATE_STUDENT_ATTENDANCE = 0x40000000000000000
    DELETE_STUDENT_ATTENDANCE = 0x80000000000000000
    FETCH_STUDENT_ATTENDANCE = 0x100000000000000000
    FETCH_STUDENT_ATTENDANCES = 0x200000000000000000

    ADMINISTER = 0x8000000000000000000000


class RoleEnum(enum.Enum):
    ANONYMOUS = 0x0000000, True
    EMPLOYEE = 0x0000000, False
    TEACHER = 0x0000000, False
    STUDENT = 0x0000000, False
    ADMINISTRATOR = 0xFFFFFFFFFFFFFFFFFFFFFF, False


class Role(db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.String(25))

    users = db.relationship("User", back_populates="role")

    @property
    def _permissions(self) -> int:
        return eval(self.permissions)

    def __init__(self) -> None:
        super().__init__()

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
                permission, default = r.value

                role.permissions, role.default = hex(permission), default

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

    def can(self, permissions):
        return (
            self.role is not None
            and (self.role._permissions & permissions) == permissions
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


@event.listens_for(User, "before_insert")
def generate_uid(*_, target):
    if target.role_uid is None:
        if target.email == current_app.config["FLASKY_ADMIN"]:
            if role := Role.query.filter_by(
                permissions=hex(RoleEnum.ADMINISTRATOR.value.__getitem__(0))
            ).first():
                target.role_uid = role.uid

        if target.role_uid is None:
            if role := Role.query.filter_by(default=True).first():
                target.role_uid = role.uid


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
