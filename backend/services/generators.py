"""
图表数据生成服务

包含所有用于前端可视化的数据生成函数
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def generate_chord_data(df):
    """生成和弦图数据（星期 -> 消费分类流向）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return {'nodes': [], 'links': []}

    weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
    expense_df['weekday'] = expense_df['交易时间'].dt.dayofweek.map(weekday_map)

    top_categories = expense_df.groupby('交易分类')['金额'].sum().nlargest(10).index.tolist()
    flow_df = expense_df[expense_df['交易分类'].isin(top_categories)]
    flow_data = flow_df.groupby(['weekday', '交易分类'])['金额'].sum()

    nodes = []
    links = []

    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    for day in weekdays:
        nodes.append({'name': day, 'category': 'weekday'})

    for cat in top_categories:
        nodes.append({'name': cat, 'category': 'category'})

    for (day, cat), amount in flow_data.items():
        if amount > 0:
            links.append({'source': day, 'target': cat, 'value': float(amount)})

    return {'nodes': nodes, 'links': links}


def generate_funnel_data(df):
    """生成漏斗图数据（按金额区间）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return []

    bins = [0, 50, 100, 500, 1000, 5000, float('inf')]
    labels = ['0-50元', '50-100元', '100-500元', '500-1000元', '1000-5000元', '>5000元']

    expense_df['amount_range'] = pd.cut(expense_df['金额'], bins=bins, labels=labels, right=False)
    funnel_data = expense_df.groupby('amount_range')['金额'].sum().reset_index()

    result = []
    for _, row in funnel_data.iterrows():
        result.append({'name': row['amount_range'], 'value': float(row['金额'])})

    result.sort(key=lambda x: x['value'], reverse=True)
    return result


def generate_quadrant_data(df):
    """生成消费象限数据（频次 vs 均价）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return []

    merchant_stats = expense_df.groupby('交易对方').agg({
        '金额': ['count', 'mean', 'sum'],
        '交易分类': lambda x: x.mode().iloc[0] if not x.mode().empty else '其他'
    }).reset_index()

    merchant_stats.columns = ['name', 'count', 'avg_amount', 'total_amount', 'category']

    filtered_stats = merchant_stats[
        (merchant_stats['total_amount'] >= 50) &
        (merchant_stats['count'] >= 2)
    ]

    data = []
    for _, row in filtered_stats.iterrows():
        data.append({
            'name': row['name'],
            'category': row['category'],
            'frequency': int(row['count']),
            'avg_amount': round(float(row['avg_amount']), 2),
            'total_amount': round(float(row['total_amount']), 2)
        })

    return data


def generate_radar_data(df):
    """生成雷达图数据（季度消费结构对比）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return {'indicator': [], 'series': []}

    top_categories = expense_df.groupby('交易分类')['金额'].sum().nlargest(8).index.tolist()

    if not top_categories:
        return {'indicator': [], 'series': []}

    expense_df['quarter'] = expense_df['交易时间'].dt.quarter
    quarters = sorted(expense_df['quarter'].unique())

    series_data = []
    max_val = 0

    for q in quarters:
        q_df = expense_df[expense_df['quarter'] == q]
        values = []
        for cat in top_categories:
            val = float(q_df[q_df['交易分类'] == cat]['金额'].sum())
            values.append(val)
            max_val = max(max_val, val)

        series_data.append({'name': f'Q{q}', 'value': values})

    indicator = [{'name': c, 'max': max_val * 1.1} for c in top_categories]

    return {'indicator': indicator, 'series': series_data}


def generate_wordcloud_data(df):
    """生成词云数据"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return []

    merchant_stats = expense_df.groupby('交易对方').agg({
        '金额': 'sum',
        '交易对方': 'count'
    }).rename(columns={'交易对方': 'count'})

    data = []
    for merchant, row in merchant_stats.iterrows():
        if row['金额'] > 10:
            data.append({'name': merchant, 'value': float(row['金额'])})

    data.sort(key=lambda x: x['value'], reverse=True)
    return data[:100]


def generate_themeriver_data(df):
    """生成河流图数据（按月统计各分类消费）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return {'categories': [], 'data': []}

    top_categories = expense_df.groupby('交易分类')['金额'].sum().nlargest(10).index.tolist()
    expense_df['month'] = expense_df['交易时间'].dt.to_period('M').astype(str)

    all_months = sorted(expense_df['month'].unique())

    data = []
    for month in all_months:
        month_df = expense_df[expense_df['month'] == month]
        for category in top_categories:
            amount = month_df[month_df['交易分类'] == category]['金额'].sum()
            data.append([month, category, float(amount)])

    return {'categories': top_categories, 'data': data}


def generate_boxplot_data(df):
    """生成消费分布箱形图数据"""
    expense_df = df[df['收/支'] == '支出'].copy()
    expense_df = expense_df[expense_df['金额'] > 0]

    if expense_df.empty:
        return {'categories': [], 'data': []}

    top_categories = expense_df.groupby('交易分类')['金额'].sum().nlargest(8).index.tolist()

    points_data = []
    box_stats = []

    for i, cat in enumerate(top_categories):
        cat_df = expense_df[expense_df['交易分类'] == cat][['金额', '交易对方', '交易时间']]
        values = cat_df['金额'].tolist()

        for _, row in cat_df.iterrows():
            points_data.append({
                'c': i,
                'v': float(row['金额']),
                'm': row['交易对方'],
                'd': row['交易时间'].strftime('%Y-%m-%d')
            })

        if values:
            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)
            box_stats.append([
                float(np.min(values)),
                float(q1),
                float(np.median(values)),
                float(q3),
                float(np.max(values))
            ])
        else:
            box_stats.append([])

    return {
        'categories': top_categories,
        'data': points_data,
        'box_data': box_stats
    }


def generate_heatmap_data(df):
    """生成热力图数据（周-小时消费节律）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return []

    expense_df['weekday'] = expense_df['交易时间'].dt.dayofweek
    expense_df['hour'] = expense_df['交易时间'].dt.hour

    heatmap_data = expense_df.groupby(['weekday', 'hour']).size().reset_index(name='count')

    data = []
    for _, row in heatmap_data.iterrows():
        data.append([int(row['hour']), int(row['weekday']), int(row['count'])])

    return data


def generate_pareto_data(df):
    """生成帕累托图数据（二八定律分析）"""
    expense_df = df[df['收/支'] == '支出'].copy()

    if expense_df.empty:
        return {'categories': [], 'values': [], 'percentages': []}

    category_stats = expense_df.groupby('交易分类')['金额'].sum().sort_values(ascending=False)

    total_amount = category_stats.sum()
    if total_amount == 0:
        return {'categories': [], 'values': [], 'percentages': []}

    cumulative_sum = category_stats.cumsum()
    cumulative_percentages = (cumulative_sum / total_amount * 100).round(2)

    top_n = 15
    categories = category_stats.index[:top_n].tolist()
    values = category_stats.values[:top_n].tolist()
    percentages = cumulative_percentages.values[:top_n].tolist()

    return {
        'categories': categories,
        'values': [float(v) for v in values],
        'percentages': percentages
    }
