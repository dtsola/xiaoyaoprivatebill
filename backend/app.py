"""
Flask 应用主入口 - 蓝图重构版本

模块化架构:
- config.py: 配置常量
- utils/: 工具函数
- parsers/: 文件解析器
- services/: 业务逻辑
- api/: API 蓝图模块
"""
import os

from flask import Flask, jsonify, send_from_directory, abort
from flask_session import Session

# ============ 导入配置 ============
from config import (
    UPLOAD_FOLDER,
    SESSION_FILE_DIR,
    MAX_CONTENT_LENGTH,
    SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE,
    SESSION_TYPE,
    SESSION_FILE_THRESHOLD,
    SESSION_FILE_MODE,
    LOG_LEVEL,
    LOG_FILE,
    LOG_FORMAT,
    DEBUG,
    HOST,
    PORT,
)

# ============ 导入工具函数 ============
from utils.session import (
    get_session_dir,
    ensure_upload_dir,
)

# ============ 导入 API 蓝图 ============
from api import register_blueprints

# ============ 创建应用 ============
app = Flask(__name__)

# ============ 应用配置 ============
app.config.update(
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY=SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE,
    SESSION_TYPE=SESSION_TYPE,
    SESSION_FILE_DIR=SESSION_FILE_DIR,
    SESSION_FILE_THRESHOLD=SESSION_FILE_THRESHOLD,
    SESSION_FILE_MODE=SESSION_FILE_MODE,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
)

# 从环境变量获取密钥
from secrets import token_hex
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or token_hex(32)

# ============ 初始化 Flask-Session ============
Session(app)

# ============ 配置日志 ============
import logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============ 注册 API 蓝图 ============
register_blueprints(app)
logger.info("API blueprints registered: files, session, analysis")

# ============ 注册新前端路由 ============
def register_new_frontend_routes():
    """注册新前端静态资源路由"""
    @app.route('/assets/<path:filename>')
    def serve_new_frontend_assets(filename):
        frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'dist')
        assets_dir = os.path.join(frontend_dist, 'assets')
        if os.path.exists(os.path.join(assets_dir, filename)):
            return send_from_directory(assets_dir, filename)
        abort(404)

register_new_frontend_routes()

# ============ 启动时初始化 ============
ensure_upload_dir()

# ============ 前端路由 ============

@app.route('/')
@app.route('/index')
def index():
    """服务新前端"""
    frontend_dist = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    if os.path.exists(frontend_dist):
        return send_from_directory(frontend_dist, 'index.html')
    return jsonify({
        'error': '前端未构建，请先运行: cd frontend && npm run build'
    }), 503


@app.route('/yearly')
@app.route('/monthly')
@app.route('/category')
@app.route('/time')
@app.route('/transactions')
@app.route('/insights')
@app.route('/settings')
def serve_frontend_routes():
    """服务新前端 - SPA 路由支持"""
    frontend_dist = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    if os.path.exists(frontend_dist):
        return send_from_directory(frontend_dist, 'index.html')
    return jsonify({'error': '前端未构建'}), 503


@app.route('/favicon.ico')
def favicon():
    """处理 favicon 请求"""
    return '', 204


# ============ 错误处理 ============

@app.errorhandler(404)
def not_found_error(error):
    return "页面未找到 - 404", 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({
        'success': False,
        'error': '服务器内部错误，请稍后重试'
    }), 500


# ============ 启动代码 ============

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host=HOST, port=PORT, debug=DEBUG)
