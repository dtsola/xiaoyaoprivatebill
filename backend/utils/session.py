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

from config import UPLOAD_FOLDER, CACHE_LIFETIME_SECONDS, SESSION_LIFETIME

logger = logging.getLogger(__name__)

# 全局缓存存储
_cache_store = {}


def get_session_dir():
    """获取当前会话的临时目录"""
    if 'user_id' not in session:
        # 使用更安全的方式生成用户ID
        session['user_id'] = f"user_{token_hex(16)}"
        # 记录会话创建时间
        session['created_at'] = datetime.now().timestamp()

    # 检查会话是否过期
    if 'created_at' in session:
        session_age = datetime.now().timestamp() - session['created_at']
        if session_age > SESSION_LIFETIME.total_seconds():  # 90分钟过期
            # 清理旧文件
            old_session_dir = os.path.join(UPLOAD_FOLDER, session['user_id'])
            if os.path.exists(old_session_dir):
                shutil.rmtree(old_session_dir)
            # 重新生成会话
            session.clear()
            return get_session_dir()

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

        # 检查缓存是否过期
        if user_id in cache:
            cache_time, cached_data = cache[user_id]
            if datetime.now().timestamp() - cache_time < CACHE_LIFETIME_SECONDS:
                return cached_data

        # 执行函数并缓存结果
        result = f(*args, **kwargs)
        cache[user_id] = (datetime.now().timestamp(), result)

        # 清理其他用户的缓存
        current_time = datetime.now().timestamp()
        expired_keys = [k for k, v in cache.items()
                       if current_time - v[0] > CACHE_LIFETIME_SECONDS]
        for k in expired_keys:
            del cache[k]

        return result

    def clear_cache(user_id):
        if user_id in cache:
            del cache[user_id]

    decorated_function.clear_cache = clear_cache

    return decorated_function


def cleanup_orphan_files():
    """清理孤儿文件：超过24小时无访问的会话目录"""
    try:
        now = datetime.now().timestamp()
        cleaned_count = 0

        # 确保上传目录存在
        if not os.path.exists(UPLOAD_FOLDER):
            return

        # 检查每个用户的临时目录
        for user_dir in os.listdir(UPLOAD_FOLDER):
            dir_path = os.path.join(UPLOAD_FOLDER, user_dir)

            if os.path.isdir(dir_path):
                # 获取目录最后修改时间
                mtime = os.path.getmtime(dir_path)
                age_hours = (now - mtime) / 3600

                # 删除超过24小时无访问的目录
                if age_hours > 24:
                    logger.info(f"清理孤儿文件: {user_dir} (未访问 {age_hours:.1f} 小时)")
                    shutil.rmtree(dir_path)
                    cleaned_count += 1

        if cleaned_count > 0:
            logger.info(f"孤儿文件清理完成: 共清理 {cleaned_count} 个目录")

    except Exception as e:
        logger.error(f"清理孤儿文件失败: {e}")


def start_cleanup_thread():
    """后台定期清理线程"""
    import threading
    from time import sleep

    def cleanup_worker():
        while True:
            sleep(3600)  # 每小时执行一次
            cleanup_orphan_files()

    thread = threading.Thread(target=cleanup_worker, daemon=True, name="OrphanFileCleanup")
    thread.start()
    logger.info("孤儿文件清理线程已启动 (每小时执行一次)")


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
