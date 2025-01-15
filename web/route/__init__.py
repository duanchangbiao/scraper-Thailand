from flask import Flask

from web.view.job import app_router as job
from web.view.user import app_router as user
from web.view.license import app_router as licenses
from web.view.auth.login import app_router as auth
from web.view.role import app_router as role
from web.view.menu import app_router as menu
from web.view.business.mor_view import app_router as mor
from web.view.business.aft_view import app_router as aft
from web.view.business.nsw_view import app_router as nsw


def init_bps(app: Flask) -> None:
    app.register_blueprint(licenses)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(role)
    app.register_blueprint(menu)
    app.register_blueprint(mor)
    app.register_blueprint(aft)
    app.register_blueprint(nsw)
    app.register_blueprint(job)