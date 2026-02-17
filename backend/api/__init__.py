"""
API 蓝图模块

包含所有 API 路由的蓝图定义：
- files: 文件上传与管理
- session: 会话管理
- analysis: 数据分析
"""
from flask import Blueprint
from .files import files_bp
from .session import session_bp
from .analysis import analysis_bp

def register_blueprints(app):
    """注册所有 API 蓝图到 Flask 应用"""
    app.register_blueprint(files_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(analysis_bp)

__all__ = ['register_blueprints', 'files_bp', 'session_bp', 'analysis_bp']