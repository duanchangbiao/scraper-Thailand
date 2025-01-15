import os

from apscheduler.schedulers.background import BackgroundScheduler


def create_app():
    from flask import Flask
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager

    from web.config import BaseConfig
    from web.extensions import init_plugs
    from web.route import init_bps
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    CORS(app, resources=r'/*')
    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图
    init_bps(app)
    JWTManager(app)
    return app
