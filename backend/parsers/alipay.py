"""
支付宝账单解析器
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parse_alipay_csv(filepath):
    """
    解析支付宝 CSV 账单文件

    Args:
        filepath: CSV 文件路径

    Returns:
        pandas.DataFrame: 解析后的数据框

    Raises:
        Exception: 解析失败时抛出异常
    """
    try:
        # 支付宝 CSV 处理逻辑 (默认 gbk)
        try:
            # 重新以 GBK 打开 (支付宝通常是 GBK)
            with open(filepath, encoding='gbk') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 如果 GBK 失败，尝试 UTF-8
            with open(filepath, encoding='utf-8') as f:
                lines = f.readlines()

        header_row = None
        status_row = None
        for i, line in enumerate(lines):
            if '交易状态' in line and not status_row:
                status_row = i
            if '交易时间' in line:
                header_row = i
                break

        if header_row is None:
            raise ValueError("无法找到支付宝账单表头行")

        # 读取数据
        try:
            df = pd.read_csv(filepath, encoding='gbk', skiprows=header_row)
            status_df = pd.read_csv(filepath, encoding='gbk', skiprows=status_row, nrows=1)
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding='utf-8', skiprows=header_row)
            status_df = pd.read_csv(filepath, encoding='utf-8', skiprows=status_row, nrows=1)

        # 获取状态列名
        status_column = status_df.columns[0]

        # 数据预处理
        df['交易时间'] = pd.to_datetime(df['交易时间'])
        df['月份'] = df['交易时间'].dt.strftime('%Y-%m')
        df['日期'] = df['交易时间'].dt.strftime('%Y-%m-%d')

        # 标记交易状态
        df['是否退款'] = df[status_column].isin(['退款成功', '交易关闭'])
        df.loc[df['是否退款'], '金额'] = -df.loc[df['是否退款'], '金额']

        # 添加来源标识
        df['来源'] = '支付宝'

        # 确保必要列存在
        if '交易对方' not in df.columns:
            df['交易对方'] = '未知'
        if '收/支' not in df.columns:
            df['收/支'] = '/'
        if '商品说明' not in df.columns:
            # 支付宝可能使用 '商品说明' 或其他列名
            if '商品' in df.columns:
                df['商品说明'] = df['商品']
            else:
                df['商品说明'] = ''
        if '交易分类' not in df.columns:
            df['交易分类'] = '其他'

        logger.info(f"成功解析支付宝账单: {len(df)} 条记录")

        return df

    except Exception as e:
        logger.error(f"解析支付宝 CSV 失败: {str(e)}")
        raise
