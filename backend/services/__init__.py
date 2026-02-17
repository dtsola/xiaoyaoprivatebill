"""
业务服务模块
"""
# 数据加载
from services.data_loader import load_alipay_data, load_demo_data, clear_data_cache

# 数据分析
from services.analysis import (
    analyze_merchants,
    analyze_scenarios,
    analyze_habits,
    analyze_latte_factor,
    analyze_nighttime_spending,
    analyze_subscriptions,
    analyze_inflation,
    analyze_brand_loyalty,
    analyze_sankey,
    analyze_engel_coefficient,
    analyze_weekend_vs_monday,
    analyze_payment_methods,
    generate_smart_tags,
    generate_story_data,
    calculate_monthly_stats,
    calculate_yearly_stats,
    calculate_change_rate,
)

# 图表数据生成
from services.generators import (
    generate_chord_data,
    generate_funnel_data,
    generate_quadrant_data,
    generate_radar_data,
    generate_wordcloud_data,
    generate_themeriver_data,
    generate_boxplot_data,
    generate_heatmap_data,
    generate_pareto_data,
)

__all__ = [
    # 数据加载
    'load_alipay_data',
    'load_demo_data',
    'clear_data_cache',
    # 数据分析
    'analyze_merchants',
    'analyze_scenarios',
    'analyze_habits',
    'analyze_latte_factor',
    'analyze_nighttime_spending',
    'analyze_subscriptions',
    'analyze_inflation',
    'analyze_brand_loyalty',
    'analyze_sankey',
    'analyze_engel_coefficient',
    'analyze_weekend_vs_monday',
    'analyze_payment_methods',
    'generate_smart_tags',
    'generate_story_data',
    'calculate_monthly_stats',
    'calculate_yearly_stats',
    'calculate_change_rate',
    # 图表数据生成
    'generate_chord_data',
    'generate_funnel_data',
    'generate_quadrant_data',
    'generate_radar_data',
    'generate_wordcloud_data',
    'generate_themeriver_data',
    'generate_boxplot_data',
    'generate_heatmap_data',
    'generate_pareto_data',
]
