"""
会话管理工具
"""
from flask import session
from datetime import datetime
from functools import wraps
from secrets import token_hex
import os
import shutil
import logging

from config import UPLOAD_FOLDER

logger = logging.getLogger(__name__)

# 全局缓存存储
_cache_store = {}


def get_session_dir():
    """获取当前会话的临时目录"""
    if 'user_id' not in session:
        # session['user_id'] = f"user_{token_hex(16)}"
        # 本地应用，使用固定的用户标识
        session['user_id'] = f"user_local"

    session_dir = os.path.join(UPLOAD_FOLDER, session['user_id'])

    if not os.path.exists(session_dir):
        os.makedirs(session_dir, mode=0o700)  # 确保目录权限正确

    return session_dir


def user_cache(f):
    """用户级别的缓存装饰器"""
    cache = _cache_store

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 演示模式下不需要缓存
        if session.get('is_demo'):
            return f(*args, **kwargs)

        # 获取当前用户ID
        user_id = session.get('user_id')
        if not user_id:
            return f(*args, **kwargs)

        # 检查缓存是否存在
        if user_id in cache:
            return cache[user_id]

        # 执行函数并缓存结果
        result = f(*args, **kwargs)
        cache[user_id] = result

        return result

    def clear_cache(user_id):
        if user_id in cache:
            del cache[user_id]

    decorated_function.clear_cache = clear_cache

    return decorated_function


def ensure_upload_dir():
    """确保必要目录存在并设置正确权限"""
    from config import SESSION_FILE_DIR

    # 上传目录
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, mode=0o700)
    else:
        os.chmod(UPLOAD_FOLDER, 0o700)

    # Session 目录 (Flask-Session)
    if not os.path.exists(SESSION_FILE_DIR):
        os.makedirs(SESSION_FILE_DIR, mode=0o700)
