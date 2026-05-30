import json
import re

from flask_wtf import FlaskForm
from wtforms import ValidationError

from app.extensions.db import db
from app.models.class_ import Class
from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job
from app.models.phone import Phone
from app.models.role import Permission, Role
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.time import Time
from app.models.user import User


class Form(FlaskForm):
    def validate_role_name(self, name):
        if Role.query.filter_by(name=name.data).first():
            raise ValidationError("A role with this name already exists.")

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

    def validate_roles(self, roles):
        roles = json.loads(roles.data)
        pattern: re.Pattern = re.compile(r"^R.\d{6}$")

        for role in roles:
            if not pattern.search(role):
                raise ValidationError(f"Not a valid Role ID.")
            elif not Role.query.filter_by(uid=role).first():
                raise ValidationError("Role with the given ID was not found :(")

    def validate_department_uid(self, department_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(department_uid.data):
            raise ValidationError("Not a valid Department UID.")
        elif not Department.query.filter_by(uid=department_uid.data).first():
            raise ValidationError("Department with the given ID was not found :(")

    def validate_head_of_department(self, head_of_department) -> None:
        h: str = head_of_department.data
        pattern: re.Pattern = re.compile(r"^(E|T).\d{6}$")

        if not pattern.search(h):
            raise ValidationError("Not a valid head of department UID.")
        elif h.startswith("E") and not Employee.query.filter_by(uid=h).first():
            raise ValidationError("Employee with the given ID was not found :(")
        elif h.startswith("T") and not Teacher.query.filter_by(uid=h).first():
            raise ValidationError("Teacher with the given ID was not found :(")

    def validate_parent_department_uid(self, parent_department_uid) -> None:
        uid: str = parent_department_uid.data
        pattern: re.Pattern = re.compile(r"^(D).\d{6}$")

        if not pattern.search(uid):
            raise ValidationError("Not a valid head of department UID.")
        elif not Department.query.filter_by(uid=uid).first():
            raise ValidationError("Department with the given ID was not found :(")

    def validate_job_uid(self, job_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(job_uid.data):
            raise ValidationError("Not a valid Job ID.")
        elif not Job.query.filter_by(uid=job_uid.data).first():
            raise ValidationError("Job with the given ID was not found :(")

    def validate_cls_name(self, name) -> None:
        if Class.query.filter_by(name=name.data).first():
            raise ValidationError("The class name must be unique :)")

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^T.\d{6}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError("Not a valid Teacher UID.")
        elif not Teacher.query.filter_by(uid=teacher_id.data).first():
            raise ValidationError("Teacher with the given ID was not found :(")

    def validate_semester_id(self, semester_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(semester_id.data):
            raise ValidationError("Not a valid Semester UID.")
        elif not Semester.query.filter_by(uid=semester_id.data).first():
            raise ValidationError("Semester with the given ID was not found :(")

    def validate_time_id(self, time_id) -> None:
        pattern: re.Pattern = re.compile(r"^T.\d{6}$")

        if not pattern.search(time_id.data):
            raise ValidationError("Not a valid Time UID.")
        elif not Time.query.filter_by(uid=time_id.data).first():
            raise ValidationError("Time with the given ID was not found :(")

    def validate_subject_id(self, subject_id) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        if not pattern.search(subject_id.data):
            raise ValidationError("Not a valid Subject UID.")
        elif not Subject.query.filter_by(uid=subject_id.data).first():
            raise ValidationError("Subject with the given ID was not found :(")

    def validate_semester_uid(self, semester_uid) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(semester_uid.data):
            raise ValidationError("Not a valid Semester UID.")
        elif not Semester.query.filter_by(uid=semester_uid.data).first():
            raise ValidationError("Semester with the given ID was not found :(")

    def validate_class_id(self, class_id) -> None:
        pattern: re.Pattern = re.compile(r"^..\d{6}$")

        if not pattern.search(class_id.data):
            raise ValidationError("Not a valid Class UID.")
        elif not Class.query.filter_by(uid=class_id.data).first():
            raise ValidationError("Class with the given ID was not found :(")

    def validate_permissions(self, permissions):
        permissions = json.loads(permissions.data)
        pattern: re.Pattern = re.compile(r"^P.\d{6}$")

        if any(filter(lambda permission: not pattern.search(permission), permissions)):
            raise ValidationError("Not a valid Permission UID.")

        for permission in permissions:
            if not Permission.query.filter_by(uid=permission).first():
                raise ValidationError("Permission with the given ID was not found :(")

    def validate_subjects(self, subjects) -> None:
        pattern: re.Pattern = re.compile(r"^S.\d{6}$")

        subjects = json.loads(subjects.data)

        for uid in subjects:
            if not pattern.search(uid):
                raise ValidationError(f"Not a valid Subject UID {uid!r}.")

            if not db.session.query(Subject).filter_by(uid=uid).count():
                raise ValidationError("Subject with the given ID was not found :(")

    # Check if username already exists
    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError("Username already taken")

    # Check if email already exists
    def validate_email(self, email):
        if self.__class__.__name__ == "SignupForm":
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already registered")
