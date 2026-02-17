"""
数据分析服务

包含所有消费数据分析函数
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime

from config import CATEGORY_COLORS

logger = logging.getLogger(__name__)


# ============ 基础分析函数 ============

def analyze_merchants(df):
    """商家消费分析"""
    expense_df = df[df['收/支'] == '支出'].copy()

    # 按商家分组统计
    merchant_stats = expense_df.groupby('交易对方').agg({
        '金额': ['count', 'sum', 'mean'],
        '交易时间': lambda x: (x.max() - x.min()).days + 1
    }).round(2)

    merchant_stats.columns = ['交易次数', '总金额', '平均金额', '交易跨度']

    # 识别常客商家
    min_count = 2 if len(df) >= 50 else 1

    frequent_merchants = []
    for merchant, group in expense_df.groupby('交易对方'):
        if len(group) >= min_count:
            frequent_merchants.append({
                'name': merchant,
                'amount': float(group['金额'].sum()),
                'count': len(group),
                'last_visit': group['交易时间'].max().strftime('%Y-%m-%d')
            })

    # 按消费金额排序
    frequent_merchants.sort(key=lambda x: x['amount'], reverse=True)

    return {
        'merchant_stats': merchant_stats.to_dict('index'),
        'frequent_merchants': frequent_merchants[:20]
    }


def analyze_scenarios(df):
    """消费场景分析"""
    expense_df = df[df['收/支'] == '支出'].copy()

    # 1. 线上/线下消费
    online_keywords = [
        '淘宝', '天猫', '京东', '拼多多', '美团', '饿了么', 'App Store', 'Steam',
        'Apple Music', 'iCloud', '网易', '支付宝', '微信', '闲鱼', '得物'
    ]
    expense_df.loc[:, '消费场景'] = expense_df['交易对方'].apply(
        lambda x: '线上' if any(k in str(x) for k in online_keywords) else '线下'
    )

    # 2. 消费时段分析
    expense_df.loc[:, '消费时段'] = expense_df['交易时间'].dt.hour.map(
        lambda x: '清晨(6-9点)' if 6 <= x < 9
        else '上午(9-12点)' if 9 <= x < 12
        else '中午(12-14点)' if 12 <= x < 14
        else '下午(14-17点)' if 14 <= x < 17
        else '傍晚(17-20点)' if 17 <= x < 20
        else '晚上(20-23点)' if 20 <= x < 23
        else '深夜(23-6点)'
    )

    # 3. 消费金额层级
    expense_df.loc[:, '消费层级'] = expense_df['金额'].map(
        lambda x: '大额(1000+)' if x >= 1000
        else '中额(300-1000)' if x >= 300
        else '小额(100-300)' if x >= 100
        else '零花(0-100)'
    )

    scenario_stats = []

    # 线上/线下统计
    for scene, amount in expense_df.groupby('消费场景')['金额'].sum().items():
        scenario_stats.append({'name': scene, 'value': float(amount), 'category': '渠道'})

    # 时段统计
    for period, amount in expense_df.groupby('消费时段')['金额'].sum().items():
        scenario_stats.append({'name': period, 'value': float(amount), 'category': '时段'})

    # 金额层级统计
    for level, amount in expense_df.groupby('消费层级')['金额'].sum().items():
        scenario_stats.append({'name': level, 'value': float(amount), 'category': '层级'})

    return scenario_stats


def analyze_habits(df):
    """消费习惯分析"""
    expense_df = df[df['收/支'] == '支出'].copy()

    daily_expenses = expense_df.groupby(expense_df['交易时间'].dt.date)['金额'].sum()
    daily_avg = float(daily_expenses.mean())
    active_days = int(len(daily_expenses))

    weekend_expenses = expense_df[expense_df['交易时间'].dt.dayofweek.isin([5, 6])]['金额'].sum()
    weekend_ratio = float((weekend_expenses / expense_df['金额'].sum() * 100))

    # 固定支出比例
    monthly_merchant_counts = expense_df.groupby(['交易对方', expense_df['交易时间'].dt.to_period('M')]).size()
    merchant_months = monthly_merchant_counts.reset_index().groupby('交易对方').size()
    total_months = len(expense_df['交易时间'].dt.to_period('M').unique())

    recurring_merchants = merchant_months[merchant_months >= max(2, total_months * 0.8)].index
    fixed_expenses = expense_df[expense_df['交易对方'].isin(recurring_merchants)]['金额'].sum()
    fixed_ratio = float((fixed_expenses / expense_df['金额'].sum() * 100)) if expense_df['金额'].sum() > 0 else 0

    month_start = expense_df[expense_df['交易时间'].dt.day <= 5]['金额'].sum()
    month_start_ratio = float((month_start / expense_df['金额'].sum() * 100)) if expense_df['金额'].sum() > 0 else 0

    return {
        'daily_avg': round(daily_avg, 2),
        'active_days': active_days,
        'weekend_ratio': round(weekend_ratio, 1),
        'fixed_expenses': round(fixed_ratio, 1),
        'month_start_ratio': round(month_start_ratio, 1)
    }


def analyze_latte_factor(df):
    """拿铁因子分析：小额高频支出"""
    expense_df = df[df['收/支'] == '支出'].copy()

    small_expenses = expense_df[expense_df['金额'] < 30]
    merchant_counts = small_expenses.groupby('交易对方').size()

    frequent_merchants = merchant_counts[merchant_counts > 5].index
    latte_df = small_expenses[small_expenses['交易对方'].isin(frequent_merchants)]

    total_amount = latte_df['金额'].sum()
    item_count = len(latte_df)

    top_merchant = merchant_counts.idxmax() if not merchant_counts.empty else "未知"

    return {
        'total_amount': float(total_amount),
        'item_count': int(item_count),
        'top_merchant': top_merchant,
        'avg_price': float(total_amount / item_count) if item_count > 0 else 0
    }


def analyze_nighttime_spending(df):
    """深夜消费分析：22:00 - 04:00"""
    expense_df = df[df['收/支'] == '支出'].copy()

    night_mask = (expense_df['交易时间'].dt.hour >= 22) | (expense_df['交易时间'].dt.hour <= 4)
    night_df = expense_df[night_mask]

    total_night_spend = night_df['金额'].sum()
    total_spend = expense_df['金额'].sum()

    top_merchant = "无"
    if not night_df.empty:
        top_merchant = night_df.groupby('交易对方')['金额'].sum().idxmax()

    return {
        'total_amount': float(total_night_spend),
        'ratio': float((total_night_spend / total_spend * 100)) if total_spend > 0 else 0,
        'top_merchant': top_merchant,
        'transaction_count': len(night_df)
    }


def analyze_subscriptions(df):
    """隐形订阅分析：每月固定扣款"""
    expense_df = df[df['收/支'] == '支出'].copy()

    monthly_spend = expense_df.groupby(['交易对方', expense_df['交易时间'].dt.to_period('M')])['金额'].sum().reset_index()
    merchant_stats = monthly_spend.groupby('交易对方')['金额'].agg(['mean', 'std', 'count'])

    subs_merchants = merchant_stats[
        (merchant_stats['count'] >= 3) &
        (merchant_stats['std'] < 5)
    ]

    subscriptions = []
    for merchant in subs_merchants.index:
        avg_amount = merchant_stats.loc[merchant, 'mean']
        subscriptions.append({
            'name': merchant,
            'monthly_amount': float(avg_amount),
            'annual_amount': float(avg_amount * 12)
        })

    subscriptions.sort(key=lambda x: x['annual_amount'], reverse=True)

    return subscriptions


def analyze_inflation(df):
    """个人通胀率：客单价变化"""
    expense_df = df[df['收/支'] == '支出'].copy()

    expense_df['quarter'] = expense_df['交易时间'].dt.to_period('Q')
    quarterly_avg = expense_df.groupby('quarter')['金额'].mean()

    if len(quarterly_avg) < 2:
        return {'trend': 'stable', 'rate': 0}

    first_q = quarterly_avg.iloc[0]
    last_q = quarterly_avg.iloc[-1]

    rate = ((last_q - first_q) / first_q * 100) if first_q > 0 else 0

    return {
        'trend': 'up' if rate > 5 else ('down' if rate < -5 else 'stable'),
        'rate': float(rate),
        'first_avg': float(first_q),
        'last_avg': float(last_q)
    }


def analyze_brand_loyalty(df):
    """品牌忠诚度分析"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return None

    top_amount_merchant = expense_df.groupby('交易对方')['金额'].sum().idxmax()
    top_amount = expense_df.groupby('交易对方')['金额'].sum().max()

    top_count_merchant = expense_df.groupby('交易对方').size().idxmax()
    top_count = expense_df.groupby('交易对方').size().max()

    return {
        'top_amount': {
            'name': top_amount_merchant,
            'value': float(top_amount)
        },
        'top_count': {
            'name': top_count_merchant,
            'value': int(top_count)
        }
    }


def analyze_sankey(df):
    """桑基图数据：分类流向"""
    expense_df = df[df['收/支'] == '支出'].copy()

    # 按分类和来源统计
    category_source = expense_df.groupby(['交易分类', '来源'])['金额'].sum().reset_index()

    nodes = []
    links = []
    node_map = {}

    # 添加来源节点
    sources = expense_df['来源'].unique()
    for i, source in enumerate(sources):
        nodes.append({'name': source, 'category': 'source'})
        node_map[source] = i

    # 添加分类节点
    categories = expense_df['交易分类'].unique()
    for i, category in enumerate(categories):
        nodes.append({'name': category, 'category': 'category'})
        node_map[category] = len(sources) + i

    # 添加链接
    for _, row in category_source.iterrows():
        source_idx = node_map[row['来源']]
        category_idx = node_map[row['交易分类']]
        links.append({
            'source': source_idx,
            'target': category_idx,
            'value': float(row['金额'])
        })

    return {'nodes': nodes, 'links': links}


def analyze_engel_coefficient(df):
    """恩格尔系数：食品支出占比"""
    expense_df = df[df['收/支'] == '支出'].copy()

    total_expense = expense_df['金额'].sum()

    # 餐饮美食分类
    food_expense = expense_df[expense_df['交易分类'] == '餐饮美食']['金额'].sum()

    engel_coefficient = (food_expense / total_expense * 100) if total_expense > 0 else 0

    return {
        'coefficient': float(engel_coefficient),
        'food_expense': float(food_expense),
        'total_expense': float(total_expense),
        'level': '富裕' if engel_coefficient < 30 else '小康' if engel_coefficient < 40 else '温饱' if engel_coefficient < 50 else '贫困'
    }


def analyze_weekend_vs_monday(df):
    """周末与周一消费对比"""
    expense_df = df[df['收/支'] == '支出'].copy()

    expense_df['day_type'] = expense_df['交易时间'].dt.dayofweek.map(
        lambda x: '周末' if x in [5, 6] else ('周一' if x == 0 else '工作日')
    )

    day_stats = []
    for day_type, group in expense_df.groupby('day_type'):
        day_stats.append({
            'day': day_type,
            'amount': float(group['金额'].sum()),
            'count': len(group),
            'avg': float(group['金额'].mean())
        })

    return day_stats


def analyze_payment_methods(df):
    """支付方式分析"""
    expense_df = df[df['收/支'] == '支出'].copy()

    # 按来源统计（支付宝/微信）
    payment_stats = expense_df.groupby('来源')['金额'].agg(['sum', 'count']).round(2)

    result = []
    for payment_method in payment_stats.index:
        result.append({
            'method': payment_method,
            'amount': float(payment_stats.loc[payment_method, 'sum']),
            'count': int(payment_stats.loc[payment_method, 'count'])
        })

    return result


def generate_smart_tags(df):
    """生成智能标签（消费画像）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    result = {
        'tags': [],
        'time_pattern': '-',
        'spending_preference': '-',
        'spending_pattern': '-',
        'spending_power': '-'
    }

    # 计算总体消费情况
    total_expense = expense_df['金额'].sum()
    avg_expense = expense_df['金额'].mean()
    daily_expense = expense_df.groupby(expense_df['交易时间'].dt.date)['金额'].sum().mean()

    # 时间模式分析
    hour_stats = expense_df.groupby(expense_df['交易时间'].dt.hour).size()
    peak_hours = hour_stats[hour_stats > hour_stats.mean()].index.tolist()

    if 22 in peak_hours or 23 in peak_hours or 0 in peak_hours:
        result['tags'].append('夜间消费达人')
        result['time_pattern'] = '您偏好在夜间消费，要注意作息哦'
    elif 6 in peak_hours or 7 in peak_hours:
        result['tags'].append('早起达人')
        result['time_pattern'] = '您是个早起消费的生活达人'
    else:
        result['time_pattern'] = '您的消费时间比较规律，集中在日间'

    # 消费偏好分析
    category_ratio = expense_df.groupby('交易分类')['金额'].sum() / total_expense
    top_categories = category_ratio[category_ratio > 0.15].index.tolist()

    preference_desc = []
    for category in top_categories:
        result['tags'].append(f'{category}控')
        preference_desc.append(f'{category}({(category_ratio[category]*100):.1f}%)')

    if preference_desc:
        result['spending_preference'] = f"最常消费的品类是{', '.join(preference_desc)}"
    else:
        result['spending_preference'] = '消费比较均衡'

    # 消费规律分析
    daily_expenses = expense_df.groupby(expense_df['交易时间'].dt.date)['金额'].sum()
    cv = daily_expenses.std() / daily_expenses.mean()

    if cv < 0.5:
        result['tags'].append('消费稳健派')
        result['spending_pattern'] = '您的消费非常有规律，是个理性消费者'
    elif cv < 0.8:
        result['tags'].append('平衡消费派')
        result['spending_pattern'] = '您的消费较为均衡，适度有波动'
    else:
        result['tags'].append('随性消费派')
        result['spending_pattern'] = '您的消费比较随性，波动较大'

    # 消费能力分析
    daily_avg = daily_expense if not pd.isna(daily_expense) else 0
    if daily_avg < 50:
        power_desc = f'日均消费{daily_avg:.0f}元，属于理性消费人群'
    elif daily_avg < 100:
        power_desc = f'日均消费{daily_avg:.0f}元，属于中等消费人群'
    else:
        power_desc = f'日均消费{daily_avg:.0f}元，属于高消费人群'
    result['spending_power'] = power_desc

    return result


def generate_story_data(df):
    """生成故事化叙述数据"""
    expense_df = df[df['收/支'] == '支出'].copy()

    total_expense = float(expense_df['金额'].sum())
    transaction_count = len(expense_df)
    avg_transaction = float(expense_df['金额'].mean())

    # 最常去的商家
    top_merchant = expense_df.groupby('交易对方')['金额'].sum().idxmax()
    top_merchant_amount = float(expense_df.groupby('交易对方')['金额'].sum().max())

    # 最喜欢的分类
    top_category = expense_df.groupby('交易分类')['金额'].sum().idxmax()
    top_category_amount = float(expense_df.groupby('交易分类')['金额'].sum().max())

    # 最忙碌的月份
    monthly_count = expense_df.groupby('月份').size()
    busiest_month = monthly_count.idxmax()
    busiest_month_count = int(monthly_count.max())

    # 单笔最大消费
    max_transaction = expense_df.loc[expense_df['金额'].idxmax()]

    return {
        'total_expense': total_expense,
        'transaction_count': transaction_count,
        'avg_transaction': avg_transaction,
        'top_merchant': {'name': top_merchant, 'amount': top_merchant_amount},
        'top_category': {'name': top_category, 'amount': top_category_amount},
        'busiest_month': {'month': busiest_month, 'count': busiest_month_count},
        'max_transaction': {
            'amount': float(max_transaction['金额']),
            'merchant': max_transaction['交易对方'],
            'date': max_transaction['交易时间'].strftime('%Y-%m-%d')
        }
    }


# ============ 辅助计算函数 ============

def calculate_monthly_stats(df):
    """计算月度统计数据"""
    if df.empty:
        return {
            'balance': 0,
            'total_expense': 0,
            'total_income': 0,
            'expense_count': 0,
            'income_count': 0,
            'total_count': 0,
            'active_days': 0,
            'avg_transaction': 0,
            'avg_daily_expense': 0,
            'expense_ratio': 0
        }

    expense_df = df[(df['收/支'] == '支出') & (~df['是否退款'])]
    income_df = df[(df['收/支'] == '收入') & (~df['是否退款'])]

    total_expense = expense_df['金额'].sum() if not expense_df.empty else 0
    total_income = income_df['金额'].sum() if not income_df.empty else 0
    active_days = len(df['日期'].unique())

    return {
        'balance': total_income - total_expense,
        'total_expense': total_expense,
        'total_income': total_income,
        'expense_count': len(expense_df),
        'income_count': len(income_df),
        'total_count': len(expense_df) + len(income_df),
        'active_days': active_days,
        'avg_transaction': round(expense_df['金额'].mean(), 2) if len(expense_df) > 0 else 0,
        'avg_daily_expense': round(total_expense / max(1, active_days), 2),
        'expense_ratio': round(total_expense / total_income * 100, 2) if total_income > 0 else 0
    }


def calculate_yearly_stats(df):
    """计算年度统计数据"""
    return calculate_monthly_stats(df)  # 使用相同的统计逻辑


def calculate_change_rate(current, previous):
    """计算环比变化率，处理特殊情况"""
    try:
        if previous == 0:
            if current == 0:
                return 0
            return None
        if current == 0:
            return -100
        return round((current - previous) / abs(previous) * 100, 2)
    except:
        return None
