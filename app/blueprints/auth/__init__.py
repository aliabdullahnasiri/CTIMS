from flask import Blueprint, flash, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions.db import db
from app.forms.login import LoginForm
from app.forms.signup import SignupForm
from app.models.permission import Permission
from app.models.user import User

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

            return redirect(
                url_for("admin.dashboard")
                if user.can(Permission.get("VIEW_DASHBOARD"))
                else url_for("admin.profile")
            )

        flash("Email or password is incorrect!", category="error")

    return render_template("auth/login.html", form=form, title="Login")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User()

        user.user_name = form.user_name.data
        user.email = form.email.data

        if passwd := form.password.data:
            user.set_password(passwd)

        user.update_roles()

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
