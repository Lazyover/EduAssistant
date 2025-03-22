from flask import Flask
from app.models.base import db
from app.config import Config
from app.react.tools_register import initialize_services

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init(app.config['DATABASE_NAME'],
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            port=app.config['DATABASE_PORT'])
    
    # 初始化工具
    initialize_services()
    
    # 注册蓝图
    from app.views.auth import auth_bp
    from app.views.dashboard import dashboard_bp
    from app.views.admin import admin_bp
    from app.views.analytics import analytics_bp
    from app.views.course import course_bp
    from app.views.search import search_bp
    from app.views.ai_assistant import ai_assistant_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(ai_assistant_bp)
    
    # 创建表
    return app