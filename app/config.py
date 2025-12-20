from __future__ import annotations

import os
import pathlib
import re

from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "Flask Application")

    SECRET_KEY = os.getenv("SECRET_KEY", "12345678")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")

    CURRENCY_SYMBOL = chr(36)

    DEFAULT_AVATAR = "admin/assets/img/default-avatar.png"

    APP_DIR = "app"

    TD_DIR = f"{APP_DIR}/templates/admin/components/tables/td"
    TD_TEMPS = [TEMP for TEMP in pathlib.Path(TD_DIR).glob("*html")]

    VIEWS_TEMPS_DIR = f"{APP_DIR}/templates/admin/views"
    VIEWS_TEMPS = [TEMP for TEMP in pathlib.Path(VIEWS_TEMPS_DIR).glob("*html")]

    UID_PATTERN: re.Pattern = re.compile(r"^(T).\d{6}$")
