from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms.login import LoginForm
from app.forms.signup import SignupForm
from app.models.user import Role, RoleEnum, User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)

            flash(f"Welcome back, {user.user_name}!", category="success")

            if current_user.is_administrator():
                return redirect(url_for("admin.dashboard"))

    return render_template("auth/login.html", form=form, title="Login")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User()

        user.user_name = form.user_name.data
        user.email = form.email.data

        user.set_password(form.password.data)

        if user.email == current_app.config["FLASKY_ADMIN"]:
            r = Role.query.filter_by(
                permissions=RoleEnum.ADMINISTRATOR.value.__getitem__(0)
            ).first()

            user.role_uid = r.uid

        if user.role is None:
            r = Role.query.filter_by(default=True).first()

            user.role_uid = r.uid

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", category="success")

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form, title="Sign Up")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("auth.login"))
