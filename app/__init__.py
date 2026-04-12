import os
import sys
from typing import Dict

from flask import Flask, current_app, url_for
from sqlalchemy import inspect

import app.const as const
from app.blueprints.admin import bp as admin_bp
from app.blueprints.api import bp as api_bp
from app.blueprints.auth import bp as auth_bp
from app.config import Config
from app.extensions.bcrypt import bcrypt
from app.extensions.db import db
from app.extensions.login_manager import login_manager
from app.extensions.migrate import migrate


def ctx() -> Dict:
    dct: Dict = {
        "PROJECT_TITLE": Config.PROJECT_TITLE,
        "DEFAULT_AVATAR_URL": url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        ),
        "DEVELOPER": const.DEVELOPER,
        "CURRENCY_SYMBOL": current_app.config["CURRENCY_SYMBOL"],
    }

    return dct


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class or Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def _():
        dct = ctx()
        return {"CURRENT_APP": current_app, "CTX": dct, **dct}

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    if "db" not in sys.argv:
        with app.app_context(), app.test_request_context():
            inspector = inspect(db.engine)

            if inspector.has_table("permissions"):
                from app.models.permission import Permission
                from app.models.role import Role

                if Permission.administer():
                    Permission.refresh()

                administrator = Role.administrator()

                for p in Permission.query.all():
                    if p not in administrator.permissions:
                        administrator.permissions.append(p)

                db.session.commit()

    return app
