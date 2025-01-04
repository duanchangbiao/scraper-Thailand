import os

from flask import Flask
from flask_cors import CORS

from app.config import BaseConfig
from app.extensions import init_plugs
from app.view import init_bps


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    CORS(app, resources=r'/*')
    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图
    init_bps(app)

    return app