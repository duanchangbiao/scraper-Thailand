import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session

from web.config import BaseConfig
from web.extensions.init_mail import init_mail
from web.extensions.init_sqlalchemy import init_databases, db
from flask_migrate import Migrate


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_session(app)
    init_migrate(app)
    init_mail(app)
    configure_logging(app)


sess = Session()


def init_session(app):
    sess.init_app(app)


from flask import Flask

migrate = Migrate()


def init_migrate(app: Flask):
    migrate.init_app(app, db)


def configure_logging(app: Flask):
    # 创建日志记录器
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.INFO)

    # 创建一个文件处理器，设置日志文件路径和最大文件大小
    file_handler = RotatingFileHandler(os.path.join(BaseConfig.LOGGER_DIR, 'log.log'), maxBytes=1024 * 1024 * 100, backupCount=10,encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 创建一个日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)

    # 配置Flask应用的日志记录器
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)