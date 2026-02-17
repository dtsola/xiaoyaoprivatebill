"""
会话管理 API 蓝图

包含以下路由:
- POST /api/demo/enter              - 进入演示模式
- POST /api/demo/exit               - 退出演示模式
- GET  /api/session/status          - 获取会话状态
- GET  /api/session/time_remaining  - 获取会话剩余时间
- POST /api/cleanup                 - 清理过期会话数据
"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, session, request
import os
import logging

from config import SESSION_LIFETIME, LOG_FILE
from utils.session import get_session_dir
from services.data_loader import clear_data_cache

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


@session_bp.route('/api/session/time_remaining')
def get_session_time_remaining():
    """获取会话剩余时间"""
    if 'created_at' not in session:
        return jsonify({'time_remaining': 0, 'formatted': '0分钟'})

    session_age = datetime.now().timestamp() - session['created_at']
    remaining = max(0, SESSION_LIFETIME.total_seconds() - session_age)

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)

    return jsonify({
        'time_remaining': int(remaining),
        'formatted': f"{minutes}分{seconds}秒"
    })


@session_bp.route('/api/cleanup', methods=['POST'])
def cleanup():
    """只在会话过期时清理数据"""
    try:
        if 'session_start' in session:
            start_time = datetime.strptime(session['session_start'], '%Y-%m-%d %H:%M:%S')
            expire_time = start_time + timedelta(minutes=SESSION_LIFETIME.total_seconds() / 60)

            if datetime.now() >= expire_time:
                if 'user_id' in session:
                    session_dir = get_session_dir()
                    if os.path.exists(session_dir):
                        import shutil
                        shutil.rmtree(session_dir)

                    if 'user_id' in session:
                        clear_data_cache()

                    session.clear()
                return jsonify({'success': True, 'message': '会话已过期,数据已清理'})

        return jsonify({'success': True, 'message': '会话未过期'})

    except Exception as e:
        logger.error(f"清理数据时出错: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
