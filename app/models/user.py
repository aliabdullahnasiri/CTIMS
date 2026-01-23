from datetime import date
from functools import wraps
from operator import call
from typing import Dict, List, Union

import humanize
from flask import abort, current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin, current_user
from numerize import numerize

from app.constants import DEFAULT_AVATAR
from app.extensions import bcrypt, db, login_manager
from app.functions import get_file_url
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
        permissions = 0x0001

        for role in self.roles.all():
            permissions |= role.hex_permissions

        return permissions

    def can(self, permissions):
        return (self.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.administer())

    def to_dict(self) -> Dict:
        dct = {
            "user_uid": getattr(self, "uid"),
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "full_name": self.full_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_src,
            "files": [f.to_dict() for f in self.files.all()],
            "phones": [p.number for p in self.phones.all()],
            **call(getattr(super(), "to_dict")),
        }

        return dct

    def get_id(self):
        return str(self.__getattribute__("uid"))

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

    @property
    def display_number_of_phone_nums(self):
        return numerize.numerize(self.phones.count())

    @property
    def display_number_of_files(self):
        return numerize.numerize(self.files.count())

    @property
    def total_file_size(self) -> str:
        return humanize.naturalsize(sum(f.size for f in self.files.all()))

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
                        if file := self.files.filter_by(id=val).scalar():
                            file.file_for = getattr(self, "uid")

    def update_roles(self, roles: Union[List[Role], None] = None):
        if self.email == current_app.config["FLASKY_ADMIN"]:
            if role := Role.administrator():
                if role not in self.roles.all():
                    self.roles.append(role)
        elif role := Role.query.filter_by(default=True).first():
            if role not in self.roles.all():
                self.roles.append(role)
        elif roles:
            for role in roles:
                if role not in self.roles.all():
                    self.roles.append(role)


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
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
