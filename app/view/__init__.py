from flask import Flask

from app.view.user import app_router as user
from app.view.license import app_router as licenses
from app.view.login import app_router as auth
from app.view.role import app_router as role
from app.view.menu import app_router as menu


def init_bps(app: Flask) -> None:
    app.register_blueprint(licenses)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(role)
    app.register_blueprint(menu)
