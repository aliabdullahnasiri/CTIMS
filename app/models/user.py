from datetime import date
from functools import wraps
from operator import call
from typing import Dict, List, Union

import humanize
from flask import abort, current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin, current_user, login_required
from numerize import numerize

from app.const import DEFAULT_AVATAR
from app.extensions.bcrypt import bcrypt
from app.extensions.db import db
from app.extensions.login_manager import login_manager
from app.func import get_file_url
from app.models.file import File, FileForEnum
from app.models.permission import Permission
from app.models.phone import Phone
from app.models.role import Role


class User(UserMixin, db.Model):
    __tablename__ = "users"

    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(128), nullable=False)

    birthday = db.Column(db.Date)

    avatar_path = db.Column(
        db.String(255),
        nullable=True,
    )

    employee = db.relationship(
        "Employee", back_populates="user", cascade="delete", uselist=False
    )
    teacher = db.relationship(
        "Teacher", back_populates="user", cascade="delete", uselist=False
    )
    student = db.relationship(
        "Student", back_populates="user", cascade="delete", uselist=False
    )

    phones = db.relationship(
        "Phone",
        back_populates="user",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    files = db.relationship(
        "File",
        back_populates="user",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    roles = db.relationship(
        "Role",
        secondary="users_roles",
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )

    @property
    def permissions(self):
        permissions = 0

        for role in self.roles.all():
            permissions |= role.hex_permissions

        return permissions

    def can(self, permissions):
        return (self.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.administer())

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
            "phones": [p.number for p in self.phones.all()],
            "roles": [r.uid for r in self.roles.all()],
            "is_deletable": not (
                self.is_administrator()
                and Role.administrator().users.count() == 1
                and self.get_id() == current_user.get_id()
            ),
            **call(getattr(super(), "to_dict")),
        }

        return dct

    def get_id(self):
        return str(self.__getattribute__("id"))

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
    def display_number_of_phone_nums(self):
        return numerize.numerize(self.phones.count())

    @property
    def display_number_of_files(self):
        return numerize.numerize(self.files.count())

    @property
    def total_file_size(self) -> str:
        return humanize.naturalsize(sum(f.size for f in self.files.all()))

    @property
    def avatar_src(self) -> str:
        u = url_for("static", filename=DEFAULT_AVATAR)

        if (
            f := self.files.filter_by(file_for=FileForEnum.AVATAR)
            .order_by(getattr(File, "created_at").desc())
            .first()
        ):
            u = f.file_url

        return u

    def update_phones(self, phones: List[str]):
        for phone in self.phones.all():
            if phone.number not in phones:
                db.session.delete(phone)

        for p in phones:
            if self.phones.filter_by(number=p).scalar():
                continue

            phone = Phone()
            phone.number = p

            self.phones.append(phone)

    def update_files(self, files: Dict[str, Union[int, List[int]]]) -> None:
        for key, value in files.items():
            match key:
                case "avatar" if type(value) == int:
                    self.avatar_path = (
                        src
                        if (src := get_file_url(value)) is not None
                        else url_for("static", filename=DEFAULT_AVATAR)
                    )

                case "files" if type(value) == list:
                    for file in self.files.filter_by(
                        file_for=getattr(self, "uid")
                    ).all():
                        if file.id not in value:
                            db.session.delete(file)

                    for val in value:
                        if file := File.query.filter_by(id=int(val)).scalar():
                            file.user = self

    def update_roles(self, roles: Union[List[int], None] = None):
        role = (
            Role.administrator()
            if self.email == current_app.config["FLASKY_ADMIN"]
            else Role.query.filter_by(default=True).first()
        )

        if role and not self.roles.filter_by(id=role.id).count():
            self.roles.append(role)
        elif type(roles) is list:
            for r in self.roles.all():
                if r.uid not in roles:
                    self.roles.remove(r)

            for role in roles:
                if role not in self.roles.all():
                    self.roles.append(role)


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(id: str):
    return User.query.filter_by(id=id).first()


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
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.can(Permission.administer()):
            abort(403)

        return f(*args, **kwargs)

    return decorated_function
