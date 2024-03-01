import os
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask_migrate import Migrate
import datetime
from config import Config, log_dir
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
cors = CORS()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../../dist',template_folder="../../dist", static_url_path='/')
    app.config.from_object(config_class)

     # 注册插件
    register_plugins(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册日志处理器
    # register_logging(app)

    # 注册错误处理函数
    # register_errors(app)

    app.logger.info('Flask Rest Api startup')
    return app


def register_plugins(app):
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):

    from app.website import website_bp
    app.register_blueprint(website_bp, url_prefix='/api/website')
