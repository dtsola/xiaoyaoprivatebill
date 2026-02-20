"""
会话管理 API 蓝图

包含以下路由:
- POST /api/demo/enter     - 进入演示模式
- POST /api/demo/exit      - 退出演示模式
- GET  /api/session/status - 获取会话状态
"""
from datetime import datetime
from flask import Blueprint, jsonify, session
import logging

from config import LOG_FILE

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建蓝图
session_bp = Blueprint('session', __name__)


@session_bp.route('/api/demo/enter', methods=['POST'])
def enter_demo_mode():
    """进入演示模式"""
    session['is_demo'] = True
    session['user_id'] = 'demo_user'
    return jsonify({'success': True})


@session_bp.route('/api/demo/exit', methods=['POST'])
def exit_demo_mode():
    """退出演示模式"""
    session.pop('is_demo', None)
    if session.get('user_id') == 'demo_user':
        session.pop('user_id', None)
    return jsonify({'success': True})


@session_bp.route('/api/session/status')
def get_session_status():
    """获取会话状态"""
    if 'user_id' not in session:
        return jsonify({'active': False, 'is_demo': False})

    return jsonify({
        'active': True,
        'is_demo': session.get('is_demo', False),
        'user_id': session.get('user_id'),
        'session_start': session.get('session_start', '')
    })


