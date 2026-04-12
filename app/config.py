from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "Flask Project")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "12345678")

    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    UPLOAD_FOLDER: str = os.path.join("app", "static", "uploads")

    FLASKY_ADMIN: str = "nasiri.aliabdullah@gmail.com"
