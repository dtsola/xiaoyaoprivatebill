"""
数据加载服务
"""
import pandas as pd
import logging
import os

from flask import session
from parsers.alipay import parse_alipay_csv
from parsers.wechat import parse_wechat_csv, parse_wechat_xlsx
from utils.file_utils import detect_file_source
from utils.session import get_session_dir

logger = logging.getLogger(__name__)


def load_demo_data():
    """
    加载演示模式数据

    Returns:
        pandas.DataFrame: 演示数据
    """
    from config import DATA_DIR

    sample_file = os.path.join(DATA_DIR, 'sample_data.csv')
    if not os.path.exists(sample_file):
        raise FileNotFoundError("示例数据文件不存在")

    df = pd.read_csv(sample_file)
    df['交易时间'] = pd.to_datetime(df['交易时间'])
    df['月份'] = df['交易时间'].dt.strftime('%Y-%m')
    df['日期'] = df['交易时间'].dt.strftime('%Y-%m-%d')

    # 确保演示数据也有这些列
    if '是否退款' not in df.columns:
        df['是否退款'] = False
    if '来源' not in df.columns:
        df['来源'] = '示例数据'

    logger.info(f"加载演示数据: {len(df)} 条记录")
    return df


def load_alipay_data():
    """
    加载并合并所有账单数据

    Returns:
        pandas.DataFrame: 合并后的数据框

    Raises:
        FileNotFoundError: 未找到任何账单文件
        Exception: 加载失败时抛出异常
    """
    try:
        # 演示模式逻辑
        if session.get('is_demo'):
            return load_demo_data()

        session_dir = get_session_dir()
        all_data = []

        # 读取会话目录中的所有文件
        for filename in os.listdir(session_dir):
            filepath = os.path.join(session_dir, filename)

            # 处理 CSV 文件
            if filename.endswith('.csv'):
                try:
                    # 判断是否为微信账单 (CSV格式)
                    is_wechat_csv = (detect_file_source(filepath) == 'wechat')

                    if is_wechat_csv:
                        df = parse_wechat_csv(filepath)
                        all_data.append(df)
                    else:
                        df = parse_alipay_csv(filepath)
                        all_data.append(df)

                except Exception as e:
                    logger.error(f"处理 CSV 文件 {filename} 失败: {str(e)}")
                    continue

            # 处理 XLSX 文件 (微信)
            elif filename.endswith('.xlsx'):
                try:
                    df = parse_wechat_xlsx(filepath)
                    all_data.append(df)
                except Exception as e:
                    logger.error(f"处理 XLSX 文件 {filename} 失败: {str(e)}")
                    continue

        if not all_data:
            raise FileNotFoundError("未找到任何支付宝(.csv)或微信(.xlsx)账单文件")

        # 合并所有数据
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.sort_values('交易时间')

        logger.info(f"加载账单数据: {len(combined_df)} 条记录")

        return combined_df

    except Exception as e:
        logger.error(f"加载数据失败: {str(e)}")
        raise


def clear_data_cache():
    """
    清除数据缓存

    Returns:
        bool: 清除成功返回 True
    """
    from utils.session import user_cache

    if 'user_id' in session:
        user_id = session['user_id']
        # 获取 load_alipay_data 函数的 clear_cache 方法
        if hasattr(load_alipay_data, 'clear_cache'):
            load_alipay_data.clear_cache(user_id)
        return True
    return False
