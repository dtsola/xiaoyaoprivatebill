"""
文件操作工具
"""
from werkzeug.utils import secure_filename
from flask import request
import os
import re
import logging
from datetime import datetime
from secrets import token_hex

from config import ALLOWED_EXTENSIONS

logger = logging.getLogger(__name__)


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_file_source(filepath):
    """检测文件是支付宝还是微信账单"""
    filename = os.path.basename(filepath)
    if filename.endswith('.xlsx'):
        return 'wechat'
    elif filename.endswith('.csv'):
        try:
            # 读取文件前1024字节判断
            with open(filepath, encoding='utf-8-sig') as f:
                content = f.read(1024)
            if '微信支付账单' in content:
                return 'wechat'
        except:
            pass
        return 'alipay'
    return 'unknown'


def save_uploaded_file(file, session_dir):
    """
    保存上传的文件

    Args:
        file: Flask FileStorage 对象
        session_dir: 会话目录路径

    Returns:
        str: 保存后的文件名
    """
    original_filename = file.filename
    safe_filename = secure_filename(original_filename)

    # 优化文件名: 去除微信导出文件名中的时间戳后缀
    # 例如: 20210401-20210630_20251216085838.xlsx -> 20210401-20210630.xlsx
    match = re.match(r'^(\d{8}-\d{8})_\d+(?:\.xlsx|\.csv)$', safe_filename)
    if match:
        base = match.group(1)
        ext = os.path.splitext(safe_filename)[1]
        safe_filename = f"{base}{ext}"

    # 处理纯中文文件名被 secure_filename 变成空或仅后缀的情况
    if not safe_filename or safe_filename.startswith('.'):
        # 如果不包含有效文件名，使用时间戳+随机字符
        ext = os.path.splitext(original_filename)[1]
        safe_filename = f"upload_{int(datetime.now().timestamp())}_{token_hex(4)}{ext}"

    # 防止同名文件覆盖，添加数字后缀
    base_name, ext = os.path.splitext(safe_filename)
    counter = 1
    filename = safe_filename
    while os.path.exists(os.path.join(session_dir, filename)):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1

    filepath = os.path.join(session_dir, filename)
    file.save(filepath)

    logger.info(f"文件已保存: {filename}")

    return filename


def format_file_size(size_bytes):
    """
    格式化文件大小显示

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        str: 格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_info(filepath):
    """
    获取文件信息

    Args:
        filepath: 文件路径

    Returns:
        dict: 包含文件名、大小、来源等信息
    """
    from utils.file_utils import detect_file_source, format_file_size

    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)

    return {
        'name': filename,
        'size': size,
        'size_formatted': format_file_size(size),
        'source': detect_file_source(filepath)
    }
