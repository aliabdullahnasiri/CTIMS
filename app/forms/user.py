import json
from operator import and_

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    DateField,
    FileField,
    HiddenField,
    MultipleFileField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, Length, Optional

from app.extensions import db
from app.models.phone import Phone
from app.models.user import User


class AddUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[Length(max=50)])
    user_name = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField("Upload new profile picture.")

    files = MultipleFileField("Files")
    phones = StringField("Phone", validators=[Optional()])

    submit = SubmitField("Add")

    # Check if username already exists
    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError("Username already taken.")

    # Check if email already exists
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered.")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(Phone)
                .filter(
                    Phone.number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")


class UpdateUserForm(AddUserForm):
    uid = HiddenField("UID", validators=[DataRequired()])
    user_uid = HiddenField("User UID", validators=[DataRequired()])

    password = PasswordField("Password")

    submit = SubmitField("Update")

    def validate_user_name(self, user_name):
        if (
            db.session.query(User)
            .filter(
                and_(User.uid != self.user_uid.data, User.user_name == user_name.data)
            )
            .first()
        ):
            raise ValidationError("Username already taken!")

    def validate_email(self, email):
        if User.query.filter(
            and_(User.uid != self.user_uid.data, User.email == email.data)
        ).first():
            raise ValidationError("Email already registered!")
