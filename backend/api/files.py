"""
文件上传与管理 API 蓝图

包含以下路由:
- POST   /api/upload           - 上传账单文件
- GET    /api/files            - 列出当前会话的文件
- DELETE /api/files/<filename> - 删除会话中的文件
- POST   /api/clear_data       - 清除所有上传文件
"""
from datetime import datetime
from flask import Blueprint, jsonify, request, session
from werkzeug.utils import secure_filename
import os
import logging

from config import LOG_FILE
from utils.session import get_session_dir
from utils.file_utils import allowed_file, save_uploaded_file, format_file_size, detect_file_source
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
files_bp = Blueprint('files', __name__)


@files_bp.route('/api/upload', methods=['POST'])
def upload_file():
    """上传账单文件"""
    try:
        logger.info("Starting file upload...")
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有文件被上传'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '未选择文件'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': '不支持的文件类型'}), 400

        session_dir = get_session_dir()
        filename = save_uploaded_file(file, session_dir)

        # 更新会话时间戳
        now_ts = datetime.now().timestamp()
        session['created_at'] = now_ts
        session['session_start'] = datetime.fromtimestamp(now_ts).strftime('%Y-%m-%d %H:%M:%S')

        # 清除数据缓存
        clear_data_cache()

        return jsonify({
            'success': True,
            'filename': filename,
            'message': '文件上传成功'
        })

    except Exception as e:
        logger.exception("Upload failed:")
        return jsonify({'success': False, 'error': str(e)}), 500


@files_bp.route('/api/files')
def list_files():
    """列出当前会话的文件"""
    session_dir = get_session_dir()
    files = []
    if os.path.exists(session_dir):
        for filename in os.listdir(session_dir):
            if filename.endswith('.csv') or filename.endswith('.xlsx'):
                filepath = os.path.join(session_dir, filename)
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'size_formatted': format_file_size(os.path.getsize(filepath)),
                    'source': detect_file_source(filepath)
                })

    files.sort(key=lambda x: x['name'])
    return jsonify({'files': files})


@files_bp.route('/api/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    """删除会话中的文件"""
    if not filename.endswith(('.csv', '.xlsx')):
        return jsonify({'success': False, 'error': '无效的文件名'})

    try:
        session_dir = get_session_dir()
        filepath = os.path.join(session_dir, secure_filename(filename))

        if os.path.exists(filepath):
            os.remove(filepath)
            clear_data_cache()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': '文件不存在'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@files_bp.route('/api/clear_data', methods=['POST'])
def clear_data():
    """清除所有上传文件"""
    try:
        import shutil
        session_dir = get_session_dir()
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
            get_session_dir()  # 重新创建目录
        clear_data_cache()
        return jsonify({'success': True, 'message': '数据已清除'})
    except Exception as e:
        logger.error(f"清除数据失败: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500