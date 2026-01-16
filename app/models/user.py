import enum
from datetime import date
from typing import Dict, List, Union

from flask import url_for
from flask_login import UserMixin

from app.constants import DEFAULT_AVATAR
from app.extensions import bcrypt, db, login_manager
from app.functions import get_file_url


@login_manager.user_loader
def load_user(uid: str):
    return User.query.filter_by(uid=uid).first()


class Role(enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    EMPLOYEE = "employee"
    GUEST = "guest"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(128), nullable=False)

    birthday = db.Column(db.Date)
    role = db.Column(db.Enum(Role), default=Role.GUEST, nullable=False)

    # Files
    avatar_path = db.Column(
        db.String(255),
        nullable=True,
    )  # Path to avatar image

    employee = db.relationship("Employee", back_populates="user", cascade="delete")

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
            "role": self.role.value,
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
