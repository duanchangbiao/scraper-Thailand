from flask import Flask
from flask_session import Session

from web.extensions.init_sqlalchemy import init_databases, db
from flask_migrate import Migrate


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_session(app)
    init_migrate(app)


sess = Session()


def init_session(app):
    sess.init_app(app)


from flask import Flask

migrate = Migrate()


def init_migrate(app: Flask):
    migrate.init_app(app, db)
