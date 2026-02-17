"""
数据验证工具
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


# 必需的数据列
REQUIRED_COLUMNS = ['交易时间', '收/支', '金额', '交易分类', '商品说明']


def validate_dataframe(df):
    """
    验证 DataFrame 是否包含必需列

    Args:
        df: pandas DataFrame

    Raises:
        ValueError: 如果缺少必需列或数据类型不正确
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"数据缺少必需列: {', '.join(missing_columns)}")

    # 验证数据类型
    if not pd.api.types.is_numeric_dtype(df['金额']):
        raise ValueError("'金额'列必须是数值类型")


def validate_amount_range(min_amount, max_amount):
    """
    验证金额范围参数

    Args:
        min_amount: 最小金额
        max_amount: 最大金额

    Returns:
        tuple: (min_amount, max_amount) 验证后的值

    Raises:
        ValueError: 如果参数无效
    """
    if min_amount is not None:
        try:
            min_amount = float(min_amount)
            if min_amount < 0:
                raise ValueError("最小金额不能为负数")
        except (ValueError, TypeError):
            raise ValueError("最小金额格式不正确")

    if max_amount is not None:
        try:
            max_amount = float(max_amount)
            if max_amount <= 0:
                raise ValueError("最大金额必须大于0")
        except (ValueError, TypeError):
            raise ValueError("最大金额格式不正确")

    # 检查范围是否有效
    if min_amount is not None and max_amount is not None:
        if min_amount >= max_amount:
            raise ValueError("最小金额必须小于最大金额")

    return min_amount, max_amount


def validate_date_params(year, month, day=None):
    """
    验证日期参数

    Args:
        year: 年份
        month: 月份
        day: 日 (可选)

    Returns:
        tuple: (year, month, day) 验证后的值

    Raises:
        ValueError: 如果参数无效
    """
    if year is not None:
        try:
            year = int(year)
            if year < 2000 or year > 2100:
                raise ValueError("年份必须在 2000-2100 之间")
        except (ValueError, TypeError):
            raise ValueError("年份格式不正确")

    if month is not None:
        try:
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("月份必须在 1-12 之间")
        except (ValueError, TypeError):
            raise ValueError("月份格式不正确")

    if day is not None:
        try:
            day = int(day)
            if day < 1 or day > 31:
                raise ValueError("日必须在 1-31 之间")
        except (ValueError, TypeError):
            raise ValueError("日格式不正确")

    return year, month, day


def validate_pagination_params(page, per_page, max_per_page=100):
    """
    验证分页参数

    Args:
        page: 页码
        per_page: 每页条数
        max_per_page: 最大每页条数

    Returns:
        tuple: (page, per_page) 验证后的值
    """
    try:
        page = int(page) if page is not None else 1
        page = max(1, page)
    except (ValueError, TypeError):
        page = 1

    try:
        per_page = int(per_page) if per_page is not None else 20
        per_page = max(1, min(per_page, max_per_page))
    except (ValueError, TypeError):
        per_page = 20

    return page, per_page
