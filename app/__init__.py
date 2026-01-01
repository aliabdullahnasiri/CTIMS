import os
from typing import Dict

from flask import Flask, current_app, request, url_for

from app.models.view import View

from .blueprints.admin import bp as admin_bp
from .blueprints.api import bp as api_bp
from .blueprints.auth import bp as auth_bp
from .config import Config
from .extensions import bcrypt, db, login_manager, migrate


def ctx() -> Dict:
    dct: Dict = {
        "PROJECT_TITLE": Config.PROJECT_TITLE,
        "DEFAULT_AVATAR_URL": url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        ),
        "DEVELOPER": "Ali Abdullah Nasiri",
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

    @app.before_request
    def _():
        if request.endpoint not in ["static"]:
            view = View()
            view.path = request.path
            view.ip_address = (request.remote_addr,)
            view.user_agent = request.headers.get("User-Agent")

            db.session.add(view)
            db.session.commit()

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
