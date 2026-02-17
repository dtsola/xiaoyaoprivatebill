"""
Flask 应用主入口 - 重构后版本

模块化架构:
- config.py: 配置常量
- utils/: 工具函数
- parsers/: 文件解析器
- services/: 业务逻辑
"""
import os
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory, abort
from flask_session import Session
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import logging
import calendar
import json
from functools import wraps

# ============ 导入配置 ============
from config import (
    UPLOAD_FOLDER,
    SESSION_FILE_DIR,
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH,
    SESSION_LIFETIME,
    SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE,
    SESSION_TYPE,
    SESSION_FILE_THRESHOLD,
    SESSION_FILE_MODE,
    LOG_LEVEL,
    LOG_FILE,
    LOG_FORMAT,
    DEBUG,
    HOST,
    PORT,
    CATEGORY_COLORS,
    DATA_DIR,
    DEFAULT_PAGE,
    DEFAULT_PER_PAGE,
    MAX_PER_PAGE,
)

# ============ 导入工具函数 ============
from utils.session import (
    get_session_dir,
    cleanup_orphan_files,
    start_cleanup_thread,
    ensure_upload_dir,
)

from utils.file_utils import (
    allowed_file,
    detect_file_source,
    save_uploaded_file,
    format_file_size,
    get_file_info,
)

from utils.validators import (
    validate_dataframe,
    validate_amount_range,
    validate_date_params,
    validate_pagination_params,
)

# ============ 导入业务服务 ============
from services.data_loader import load_alipay_data, clear_data_cache
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

# ============ 创建应用 ============
app = Flask(__name__)

# ============ 应用配置 ============
app.config.update(
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY=SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE,
    PERMANENT_SESSION_LIFETIME=SESSION_LIFETIME,
    SESSION_TYPE=SESSION_TYPE,
    SESSION_FILE_DIR=SESSION_FILE_DIR,
    SESSION_FILE_THRESHOLD=SESSION_FILE_THRESHOLD,
    SESSION_FILE_MODE=SESSION_FILE_MODE,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
)

# 从环境变量获取密钥
from secrets import token_hex
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or token_hex(32)

# ============ 初始化 Flask-Session ============
Session(app)

# ============ 配置日志 ============
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============ 注册新前端路由 ============
def register_new_frontend_routes():
    """注册新前端静态资源路由"""
    @app.route('/assets/<path:filename>')
    def serve_new_frontend_assets(filename):
        frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'dist')
        assets_dir = os.path.join(frontend_dist, 'assets')
        if os.path.exists(os.path.join(assets_dir, filename)):
            return send_from_directory(assets_dir, filename)
        from flask import abort
        abort(404)

register_new_frontend_routes()

# ============ 启动时初始化 ============
ensure_upload_dir()
cleanup_orphan_files()
start_cleanup_thread()

# ============ 前端路由 ============

@app.route('/')
@app.route('/index')
def index():
    """服务新前端"""
    frontend_dist = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    if os.path.exists(frontend_dist):
        return send_from_directory(frontend_dist, 'index.html')
    return jsonify({
        'error': '前端未构建，请先运行: cd frontend && npm run build'
    }), 503


@app.route('/yearly')
@app.route('/monthly')
@app.route('/category')
@app.route('/time')
@app.route('/transactions')
@app.route('/insights')
@app.route('/settings')
def serve_frontend_routes():
    """服务新前端 - SPA 路由支持"""
    frontend_dist = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    if os.path.exists(frontend_dist):
        return send_from_directory(frontend_dist, 'index.html')
    return jsonify({'error': '前端未构建'}), 503


@app.route('/favicon.ico')
def favicon():
    """处理 favicon 请求"""
    return '', 204


# ============ API 路由 ============

@app.route('/api/analysis')
def get_analysis():
    """综合分析 API"""
    try:
        df = load_alipay_data()

        year = request.args.get('year', type=int)
        if year:
            df = df[df['交易时间'].dt.year == year]

        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)

        if min_amount:
            df = df[df['金额'] >= min_amount]
        if max_amount:
            df = df[df['金额'] < max_amount]

        return jsonify({
            'success': True,
            'data': {
                'merchant_analysis': analyze_merchants(df),
                'scenario_analysis': analyze_scenarios(df),
                'habit_analysis': analyze_habits(df),
                'latte_factor': analyze_latte_factor(df),
                'nighttime_analysis': analyze_nighttime_spending(df),
                'subscription_analysis': analyze_subscriptions(df),
                'inflation_analysis': analyze_inflation(df),
                'brand_loyalty': analyze_brand_loyalty(df),
                'sankey_data': analyze_sankey(df),
                'engel_coefficient': analyze_engel_coefficient(df),
                'weekend_monday': analyze_weekend_vs_monday(df),
                'story_data': generate_story_data(df),
                'tags': generate_smart_tags(df),
                'payment_analysis': analyze_payment_methods(df),
                'chord_data': generate_chord_data(df),
                'funnel_data': generate_funnel_data(df),
                'quadrant_data': generate_quadrant_data(df),
                'radar_data': generate_radar_data(df),
                'wordcloud_data': generate_wordcloud_data(df),
                'themeriver_data': generate_themeriver_data(df),
                'boxplot_data': generate_boxplot_data(df),
                'heatmap_data': generate_heatmap_data(df),
                'pareto_data': generate_pareto_data(df)
            }
        })

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


# ============ 文件上传 API ============

@app.route('/api/upload', methods=['POST'])
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


@app.route('/api/files')
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


@app.route('/api/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    """删除会话中的文件"""
    if not filename.endswith(('.csv', '.xlsx')):
        return jsonify({'success': False, 'error': '无效的文件名'})

    try:
        from werkzeug.utils import secure_filename
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


@app.route('/api/clear_data', methods=['POST'])
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


# ============ 会话管理 API ============

@app.route('/api/demo/enter', methods=['POST'])
def enter_demo_mode():
    session['is_demo'] = True
    session['user_id'] = 'demo_user'
    return jsonify({'success': True})


@app.route('/api/demo/exit', methods=['POST'])
def exit_demo_mode():
    session.pop('is_demo', None)
    if session.get('user_id') == 'demo_user':
        session.pop('user_id', None)
    return jsonify({'success': True})


@app.route('/api/session/status')
def get_session_status():
    """获取会话状态"""
    if 'user_id' not in session:
        return jsonify({'active': False, 'is_demo': False})

    return jsonify({
        'active': True,
        'is_demo': session.get('is_demo', False),
        'user_id': session.get('user_id'),
        'session_start': session.get('session_start', '')
    })


@app.route('/api/session/time_remaining')
def get_session_time_remaining():
    """获取会话剩余时间"""
    if 'created_at' not in session:
        return jsonify({'time_remaining': 0, 'formatted': '0分钟'})

    session_age = datetime.now().timestamp() - session['created_at']
    remaining = max(0, SESSION_LIFETIME.total_seconds() - session_age)

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)

    return jsonify({
        'time_remaining': int(remaining),
        'formatted': f"{minutes}分{seconds}秒"
    })


@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """只在会话过期时清理数据"""
    try:
        if 'session_start' in session:
            start_time = datetime.strptime(session['session_start'], '%Y-%m-%d %H:%M:%S')
            expire_time = start_time + timedelta(minutes=SESSION_LIFETIME.total_seconds() / 60)

            if datetime.now() >= expire_time:
                if 'user_id' in session:
                    session_dir = get_session_dir()
                    if os.path.exists(session_dir):
                        import shutil
                        shutil.rmtree(session_dir)

                    if 'user_id' in session:
                        clear_data_cache()

                    session.clear()
                return jsonify({'success': True, 'message': '会话已过期,数据已清理'})

        return jsonify({'success': True, 'message': '会话未过期'})

    except Exception as e:
        logger.error(f"清理数据时出错: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ 数据分析 API ============

@app.route('/api/yearly_analysis')
def yearly_analysis():
    """年度分析 API"""
    try:
        df = load_alipay_data()
        year = request.args.get('year', type=int)
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)

        # 获取当前年份数据
        current_year_df = df[df['交易时间'].dt.year == year] if year else df

        # 获取上一年数据
        last_year = year - 1 if year else df['交易时间'].dt.year.max() - 1
        last_year_df = df[df['交易时间'].dt.year == last_year]

        # 应用金额筛选
        if min_amount:
            current_year_df = current_year_df[current_year_df['金额'] >= min_amount]
            last_year_df = last_year_df[last_year_df['金额'] >= min_amount]
        if max_amount:
            current_year_df = current_year_df[current_year_df['金额'] < max_amount]
            last_year_df = last_year_df[last_year_df['金额'] < max_amount]

        # 过滤有效交易
        current_expense_df = current_year_df[
            (current_year_df['收/支'] == '支出') &
            (~current_year_df['是否退款'])
        ]
        current_income_df = current_year_df[
            (current_year_df['收/支'] == '收入') &
            (~current_year_df['是否退款'])
        ]

        last_expense_df = last_year_df[
            (last_year_df['收/支'] == '支出') &
            (~last_year_df['是否退款'])
        ]
        last_income_df = last_year_df[
            (last_year_df['收/支'] == '收入') &
            (~last_year_df['是否退款'])
        ]

        # 计算当前年份数据
        current_expense = current_expense_df['金额'].sum()
        current_income = current_income_df['金额'].sum()
        current_balance = current_income - current_expense

        # 计算上一年数据
        last_expense = last_expense_df['金额'].sum()
        last_income = last_income_df['金额'].sum()
        last_balance = last_income - last_expense

        # 生成完整的月份列表
        all_months = [f"{year}-{str(month).zfill(2)}" for month in range(1, 13)]

        # 按月统计支出和收入
        monthly_expenses = current_expense_df.groupby(
            current_expense_df['交易时间'].dt.strftime('%Y-%m')
        )['金额'].sum()
        monthly_incomes = current_income_df.groupby(
            current_income_df['交易时间'].dt.strftime('%Y-%m')
        )['金额'].sum()

        monthly_expenses = monthly_expenses.reindex(all_months, fill_value=0)
        monthly_incomes = monthly_incomes.reindex(all_months, fill_value=0)

        # 计算分类统计
        category_expenses = current_expense_df.groupby('交易分类')['金额'].sum()
        category_incomes = current_income_df.groupby('交易分类')['金额'].sum()

        # 计算分来源的分类统计
        expense_source = current_expense_df.groupby(['来源', '交易分类'])['金额'].sum().reset_index().to_dict('records')
        income_source = current_income_df.groupby(['来源', '交易分类'])['金额'].sum().reset_index().to_dict('records')

        # 计算年度统计数据
        yearly_stats = {
            'balance': float(current_balance),
            'total_expense': float(current_expense),
            'total_income': float(current_income),
            'expense_count': int(len(current_expense_df)),
            'income_count': int(len(current_income_df)),
            'total_count': int(len(current_expense_df) + len(current_income_df)),
            'active_days': int(len(current_year_df['交易时间'].dt.date.unique())),
            'avg_transaction': float(current_expense_df['金额'].mean()) if len(current_expense_df) > 0 else 0,
            'avg_daily_expense': float(current_expense / max(1, len(current_year_df['交易时间'].dt.date.unique()))),
            'avg_monthly_income': float(current_income / 12),
            'expense_ratio': float(current_expense / current_income * 100) if current_income > 0 else 0,
            'comparisons': {
                'balance': {
                    'change': float(current_balance - last_balance) if len(last_year_df) > 0 else None,
                    'rate': float((current_balance - last_balance) / abs(last_balance) * 100) if len(last_year_df) > 0 and last_balance != 0 else None
                },
                'expense': {
                    'change': float(current_expense - last_expense) if len(last_year_df) > 0 else None,
                    'rate': float((current_expense - last_expense) / last_expense * 100) if len(last_year_df) > 0 and last_expense != 0 else None
                },
                'income': {
                    'change': float(current_income - last_income) if len(last_year_df) > 0 else None,
                    'rate': float((current_income - last_income) / last_income * 100) if len(last_year_df) > 0 and last_income != 0 else None
                },
                'count': {
                    'change': int(len(current_expense_df) + len(current_income_df) - len(last_expense_df) - len(last_income_df)) if len(last_year_df) > 0 else None,
                    'rate': float((len(current_expense_df) + len(current_income_df) - len(last_expense_df) - len(last_income_df)) / (len(last_expense_df) + len(last_income_df)) * 100) if len(last_year_df) > 0 and (len(last_expense_df) + len(last_income_df)) != 0 else None
                }
            }
        }

        logger.info(f"Yearly stats: income={current_income}, expense={current_expense}, balance={current_balance}")

        return jsonify({
            'success': True,
            'data': {
                'trends': {
                    'months': monthly_expenses.index.tolist(),
                    'expenses': monthly_expenses.values.tolist(),
                    'incomes': monthly_incomes.values.tolist()
                },
                'categories': {
                    'expense': {
                        'names': category_expenses.index.tolist(),
                        'amounts': category_expenses.values.tolist()
                    },
                    'income': {
                        'names': category_incomes.index.tolist(),
                        'amounts': category_incomes.values.tolist()
                    }
                },
                'categories_source': {
                    'expense': expense_source,
                    'income': income_source
                },
                'yearly_stats': yearly_stats
            }
        })

    except Exception as e:
        logger.error(f"Error in yearly analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/monthly_analysis')
def monthly_analysis():
    """月度分析 API"""
    try:
        df = load_alipay_data()
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)

        # 获取当前月份数据
        current_month_df = df[
            (df['交易时间'].dt.year == year) &
            (df['交易时间'].dt.month == month)
        ]

        # 获取上月数据
        last_month = month - 1 if month > 1 else 12
        last_year = year if month > 1 else year - 1
        last_month_df = df[
            (df['交易时间'].dt.year == last_year) &
            (df['交易时间'].dt.month == last_month)
        ]

        # 应用金额筛选
        if min_amount:
            current_month_df = current_month_df[current_month_df['金额'] >= min_amount]
            last_month_df = last_month_df[last_month_df['金额'] >= min_amount]
        if max_amount:
            current_month_df = current_month_df[current_month_df['金额'] < max_amount]
            last_month_df = last_month_df[last_month_df['金额'] < max_amount]

        # 处理收入和支出数据
        current_expense_df = current_month_df[
            (current_month_df['收/支'] == '支出') &
            (~current_month_df['是否退款'])
        ]
        current_income_df = current_month_df[
            (current_month_df['收/支'] == '收入') &
            (~current_month_df['是否退款'])
        ]

        # 计算统计数据
        current_expense = current_expense_df['金额'].sum()
        current_income = current_income_df['金额'].sum()
        current_balance = current_income - current_expense

        # 计算上月数据
        last_expense = last_month_df[
            (last_month_df['收/支'] == '支出') &
            (~last_month_df['是否退款'])
        ]['金额'].sum()
        last_income = last_month_df[
            (last_month_df['收/支'] == '收入') &
            (~last_month_df['是否退款'])
        ]['金额'].sum()
        last_balance = last_income - last_expense

        # 按日期统计
        daily_expenses = current_expense_df.groupby(
            current_expense_df['交易时间'].dt.date
        )['金额'].sum()
        daily_incomes = current_income_df.groupby(
            current_income_df['交易时间'].dt.date
        )['金额'].sum()

        # 计算分类统计
        expense_categories = current_expense_df.groupby('交易分类')['金额'].sum()
        income_categories = current_income_df.groupby('交易分类')['金额'].sum()

        # 计算分来源的分类统计
        expense_source = current_expense_df.groupby(['来源', '交易分类'])['金额'].sum().reset_index().to_dict('records')
        income_source = current_income_df.groupby(['来源', '交易分类'])['金额'].sum().reset_index().to_dict('records')

        # 生成当月所有日期
        last_day = calendar.monthrange(year, month)[1]
        all_dates = [
            datetime(year, month, day).date()
            for day in range(1, last_day + 1)
        ]

        # 补充所有日期，缺失的填充0
        daily_expenses = daily_expenses.reindex(all_dates, fill_value=0)
        daily_incomes = daily_incomes.reindex(all_dates, fill_value=0)

        return jsonify({
            'success': True,
            'data': {
                'stats': {
                    'balance': float(current_balance),
                    'total_expense': float(current_expense),
                    'total_income': float(current_income),
                    'expense_count': int(len(current_expense_df)),
                    'income_count': int(len(current_income_df)),
                    'comparisons': {
                        'balance': {
                            'change': float(current_balance - last_balance),
                            'rate': float((current_balance - last_balance) / abs(last_balance) * 100) if last_balance != 0 else None
                        },
                        'expense': {
                            'change': float(current_expense - last_expense),
                            'rate': float((current_expense - last_expense) / last_expense * 100) if last_expense != 0 else None
                        },
                        'income': {
                            'change': float(current_income - last_income),
                            'rate': float((current_income - last_income) / last_income * 100) if last_income != 0 else None
                        }
                    }
                },
                'daily_data': {
                    'expense': {
                        'dates': [d.strftime('%Y-%m-%d') for d in all_dates],
                        'amounts': daily_expenses.values.tolist()
                    },
                    'income': {
                        'dates': [d.strftime('%Y-%m-%d') for d in all_dates],
                        'amounts': daily_incomes.values.tolist()
                    }
                },
                'categories': {
                    'expense': {
                        'names': expense_categories.index.tolist(),
                        'amounts': expense_categories.values.tolist()
                    },
                    'income': {
                        'names': income_categories.index.tolist(),
                        'amounts': income_categories.values.tolist()
                    }
                },
                'categories_source': {
                    'expense': expense_source,
                    'income': income_source
                }
            }
        })

    except Exception as e:
        logger.error(f"Error in monthly analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/category_expenses')
def category_expenses():
    """获取分类支出统计"""
    df = load_alipay_data()

    category_stats = df[df['收/支'] == '支出'].groupby('交易分类').agg({
        '金额': 'sum'
    }).sort_values('金额', ascending=False)

    return jsonify({
        'categories': category_stats.index.tolist(),
        'amounts': category_stats['金额'].tolist()
    })


@app.route('/api/transactions')
def get_transactions():
    """获取交易记录列表（支持分页和筛选）"""
    try:
        df = load_alipay_data()

        page = request.args.get('page', DEFAULT_PAGE, type=int)
        per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)
        per_page = min(per_page, MAX_PER_PAGE)

        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        date = request.args.get('date')
        hour = request.args.get('hour', type=int)
        category = request.args.get('category')
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        type_ = request.args.get('type')
        search_query = request.args.get('search')

        # 应用筛选条件
        if type_:
            df = df[df['收/支'] == type_]

        if search_query:
            mask = (
                df['商品说明'].astype(str).str.contains(search_query, case=False, na=False) |
                df['交易对方'].astype(str).str.contains(search_query, case=False, na=False) |
                df['交易分类'].astype(str).str.contains(search_query, case=False, na=False)
            )
            df = df[mask]

        if year:
            df = df[df['交易时间'].dt.year == year]
        if month:
            df = df[df['交易时间'].dt.month == month]
        if date:
            df = df[df['日期'] == date]
        if hour is not None:
            df = df[df['交易时间'].dt.hour == hour]
        if category:
            df = df[df['交易分类'] == category]
        if min_amount:
            df = df[df['金额'] >= min_amount]
        if max_amount:
            df = df[df['金额'] <= max_amount]

        df = df[df['收/支'].isin(['收入', '支出'])]
        df = df[~df['是否退款']]
        df = df.sort_values('交易时间', ascending=False)

        total_records = len(df)
        total_pages = (total_records + per_page - 1) // per_page
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_records)

        page_df = df.iloc[start_idx:end_idx]

        transactions = []
        for _, row in page_df.iterrows():
            transactions.append({
                'time': row['交易时间'].strftime('%Y-%m-%d %H:%M:%S'),
                'description': str(row['商品说明']),
                'category': str(row['交易分类']),
                'type': str(row['收/支']),
                'amount': float(row['金额']),
                'status': str(row['交易状态']),
                'counterparty': str(row.get('交易对方', '')) if pd.notna(row.get('交易对方')) else ''
            })

        return jsonify({
            'success': True,
            'transactions': transactions,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'total_records': total_records
            }
        })

    except Exception as e:
        logger.error(f"获取交易记录时出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'获取交易记录失败: {str(e)}'
        }), 500


@app.route('/api/summary')
def summary():
    """获取汇总数据"""
    df = load_alipay_data()

    current_date = datetime.now()
    current_month = current_date.strftime('%Y-%m')

    expense_df = df[df['收/支'] == '支出']
    total_expense = expense_df['金额'].sum()
    total_income = df[df['收/支'] == '收入']['金额'].sum()

    monthly_expenses = expense_df.groupby('月份')['金额'].sum()

    latest_month = monthly_expenses.index[-1]
    latest_month_expense = monthly_expenses[latest_month]

    current_month_expense = monthly_expenses.get(current_month)

    display_month = current_month if current_month_expense is not None else latest_month
    display_expense = current_month_expense if current_month_expense is not None else latest_month_expense

    if len(monthly_expenses) > 1:
        prev_month_expense = monthly_expenses.iloc[-2]
    else:
        prev_month_expense = display_expense

    return jsonify({
        'total_expense': round(total_expense, 2),
        'total_income': round(total_income, 2),
        'balance': round(total_income - total_expense, 2),
        'monthly_avg': round(monthly_expenses.mean(), 2),
        'current_month_expense': round(display_expense, 2),
        'prev_monthly_avg': round(prev_month_expense, 2),
        'month_count': len(monthly_expenses),
        'transaction_count': len(expense_df),
        'current_month': display_month,
        'has_current_month_data': current_month_expense is not None
    })


@app.route('/api/daily_data')
def daily_data():
    """获取热力图数据"""
    try:
        df = load_alipay_data()

        year = request.args.get('year', type=int)
        filter_type = request.args.get('filter', 'all')

        if filter_type == 'large':
            df = df[df['金额'] > 1000]
        elif filter_type == 'small':
            df = df[df['金额'] <= 1000]

        if year:
            df = df[df['交易时间'].dt.year == year]

        df = df[df['收/支'].isin(['收入', '支出'])]

        daily_data = df.groupby(['日期', '收/支']).agg({
            '金额': 'sum',
            '交易时间': 'count'
        }).reset_index()

        expense_data = []
        income_data = []
        transaction_data = []

        for date, group in daily_data.groupby('日期'):
            expense = group[group['收/支'] == '支出']
            if not expense.empty:
                expense_data.append([date, float(expense['金额'].iloc[0])])

            income = group[group['收/支'] == '收入']
            if not income.empty:
                income_data.append([date, float(income['金额'].iloc[0])])

            transaction_count = group['交易时间'].sum()
            transaction_data.append([date, int(transaction_count)])

        expense_amounts = [x[1] for x in expense_data]
        income_amounts = [x[1] for x in income_data]

        expense_quantiles = []
        income_quantiles = []

        if expense_amounts:
            expense_quantiles = [
                round(float(x), 2) for x in np.quantile(expense_amounts, [0.2, 0.4, 0.6, 0.8])
            ]

        if income_amounts:
            income_quantiles = [
                round(float(x), 2) for x in np.quantile(income_amounts, [0.2, 0.4, 0.6, 0.8])
            ]

        return jsonify({
            'expense': expense_data,
            'income': income_data,
            'transaction': transaction_data,
            'expense_quantiles': expense_quantiles,
            'income_quantiles': income_quantiles
        })

    except Exception as e:
        logger.error(f"Error in daily data: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/category_detail/<month>/<category>')
def category_detail(month, category):
    """获取指定月份和分类的支出明细"""
    df = load_alipay_data()

    details = df[
        (df['月份'] == month) &
        (df['交易分类'] == category) &
        (df['收/支'] == '支出')
    ].sort_values('金额', ascending=False)[
        ['交易时间', '商品说明', '交易对方', '金额', '交易状态']
    ].to_dict('records')

    formatted_details = [{
        'time': detail['交易时间'].strftime('%Y-%m-%d %H:%M:%S'),
        'description': detail['商品说明'],
        'counterparty': detail['交易对方'],
        'amount': round(float(detail['金额']), 2),
        'status': detail['交易状态']
    } for detail in details]

    return jsonify(formatted_details)


@app.route('/api/top_transactions')
def get_top_transactions():
    """获取大额交易记录"""
    try:
        limit = int(request.args.get('limit', 10))
        min_amount = float(request.args.get('min_amount', 1000))

        df = load_alipay_data()

        expense_df = df[df['收/支'] == '支出'].copy()
        large_transactions = expense_df[expense_df['金额'] >= min_amount]
        top_transactions = large_transactions.nlargest(limit, '金额')

        transactions = []
        for _, row in top_transactions.iterrows():
            transactions.append({
                'time': row['交易时间'].strftime('%Y-%m-%d %H:%M:%S'),
                'date': row['交易时间'].strftime('%Y-%m-%d'),
                'category': row['交易分类'],
                'description': row['商品说明'],
                'amount': float(row['金额']),
                'status': row['交易状态'],
                'counterparty': row.get('交易对方', '')
            })

        return jsonify({
            'success': True,
            'transactions': transactions
        })

    except Exception as e:
        logger.error(f"获取大额交易记录时出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'获取大额交易记录失败: {str(e)}'
        }), 500


@app.route('/api/category_trend/<category>')
def category_trend(category):
    """获取指定分类的月度趋势"""
    df = load_alipay_data()

    category_df = df[
        (df['收/支'] == '支出') &
        (df['交易分类'] == category)
    ]

    monthly_stats = category_df.groupby('月份').agg({
        '金额': ['sum', 'count', 'mean'],
        '交易时间': lambda x: len(x.dt.date.unique())
    }).round(2)

    monthly_stats.columns = ['total', 'transactions', 'avg_amount', 'active_days']

    monthly_stats['daily_avg'] = (monthly_stats['total'] / monthly_stats['active_days']).round(2)
    monthly_stats['mom_rate'] = (monthly_stats['total'].pct_change() * 100).round(2)

    total_expense = df[
        (df['收/支'] == '支出')
    ].groupby('月份')['金额'].sum()
    monthly_stats['percentage'] = (monthly_stats['total'] / total_expense * 100).round(2)

    return jsonify({
        'months': monthly_stats.index.tolist(),
        'total': monthly_stats['total'].tolist(),
        'transactions': monthly_stats['transactions'].tolist(),
        'avg_amount': monthly_stats['avg_amount'].tolist(),
        'daily_avg': monthly_stats['daily_avg'].tolist(),
        'mom_rate': monthly_stats['mom_rate'].fillna(0).tolist(),
        'percentage': monthly_stats['percentage'].tolist(),
        'summary': {
            'total_amount': category_df['金额'].sum().round(2),
            'total_transactions': len(category_df),
            'max_month': monthly_stats['total'].idxmax(),
            'max_amount': monthly_stats['total'].max().round(2),
            'min_month': monthly_stats['total'].idxmin(),
            'min_amount': monthly_stats['total'].min().round(2),
            'avg_monthly': monthly_stats['total'].mean().round(2)
        }
    })


@app.route('/api/time_analysis')
def time_analysis():
    """获取时间分析数据"""
    try:
        df = load_alipay_data()

        year = request.args.get('year', type=int)
        filter_type = request.args.get('filter', 'all')

        expense_df = df[(df['收/支'] == '支出') & (~df['是否退款'])]
        expense_df = expense_df[expense_df['金额'] > 0]

        if year:
            expense_df = expense_df[expense_df['交易时间'].dt.year == year]

        if filter_type == 'large':
            expense_df = expense_df[expense_df['金额'] > 1000]
        elif filter_type == 'small':
            expense_df = expense_df[expense_df['金额'] <= 1000]

        # 计算日内时段分布
        expense_df['hour'] = expense_df['交易时间'].dt.hour
        hourly_stats = expense_df.groupby('hour').agg({
            '金额': 'sum',
            '交易时间': 'count'
        }).reset_index()

        all_hours = pd.DataFrame({'hour': range(24)})
        hourly_stats = pd.merge(all_hours, hourly_stats, on='hour', how='left').fillna(0)

        hourly_data = {
            'amounts': hourly_stats['金额'].round(2).tolist(),
            'counts': hourly_stats['交易时间'].tolist()
        }

        # 计算工作日/周末分布
        expense_df['is_weekend'] = expense_df['交易时间'].dt.dayofweek.isin([5, 6])
        category_weekday = {}

        for category in expense_df['交易分类'].unique():
            category_df = expense_df[expense_df['交易分类'] == category]

            if len(category_df) == 0:
                continue

            weekday_amount = category_df[~category_df['is_weekend']]['金额'].sum()
            weekend_amount = category_df[category_df['is_weekend']]['金额'].sum()
            total_amount = weekday_amount + weekend_amount

            if total_amount == 0:
                continue

            weekday_count = len(category_df[~category_df['is_weekend']])
            weekend_count = len(category_df[category_df['is_weekend']])

            category_weekday[category] = {
                'weekday': {
                    'amount': float(weekday_amount),
                    'count': int(weekday_count),
                    'percentage': round(weekday_amount / total_amount * 100, 1)
                },
                'weekend': {
                    'amount': float(weekend_amount),
                    'count': int(weekend_count),
                    'percentage': round(weekend_amount / total_amount * 100, 1)
                }
            }

        sorted_categories = sorted(
            category_weekday.items(),
            key=lambda x: x[1]['weekday']['amount'] + x[1]['weekend']['amount'],
            reverse=True
        )
        category_weekday = dict(sorted_categories)

        return jsonify({
            'hourly': hourly_data,
            'weekday_weekend': category_weekday
        })

    except Exception as e:
        logger.error(f"Error in time analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/filtered_monthly_analysis')
def filtered_monthly_analysis():
    """获取过滤后的月度分析"""
    df = load_alipay_data()
    filter_type = request.args.get('filter', 'all')

    expense_df = df[(df['收/支'] == '支出') & (~df['是否退款'])]
    expense_df = expense_df[expense_df['金额'] > 0]

    if filter_type == 'large':
        expense_df = expense_df[expense_df['金额'] > 1000]
    elif filter_type == 'small':
        expense_df = expense_df[expense_df['金额'] <= 1000]

    monthly_stats = expense_df.groupby('月份').agg({
        '金额': ['sum', 'count', 'mean'],
        '交易时间': lambda x: len(x.dt.date.unique())
    }).round(2)

    monthly_stats.columns = ['total', 'count', 'avg_amount', 'active_days']

    monthly_stats['daily_avg'] = (monthly_stats['total'] / monthly_stats['active_days']).round(2)
    monthly_stats['mom_rate'] = (monthly_stats['total'].pct_change() * 100).round(2)
    monthly_stats['moving_avg'] = monthly_stats['total'].rolling(3, min_periods=1).mean().round(2)

    category_expenses = expense_df.pivot_table(
        index='月份',
        columns='交易分类',
        values='金额',
        aggfunc='sum',
        fill_value=0
    )

    return jsonify({
        'months': monthly_stats.index.tolist(),
        'total_expenses': monthly_stats['total'].tolist(),
        'transaction_counts': monthly_stats['count'].tolist(),
        'daily_averages': monthly_stats['daily_avg'].tolist(),
        'mom_rates': monthly_stats['mom_rate'].fillna(0).tolist(),
        'moving_averages': monthly_stats['moving_avg'].tolist(),
        'categories': category_expenses.columns.tolist(),
        'category_expenses': category_expenses.values.tolist()
    })


@app.route('/api/overview_data')
def get_overview_data():
    """获取概览数据"""
    try:
        df = load_alipay_data()

        filter_type = request.args.get('filter', 'all')
        year = request.args.get('year', None)

        if year is None:
            year = str(df['交易时间'].max().year)

        year_df = df[df['交易时间'].dt.year == int(year)]

        if filter_type == 'large':
            year_df = year_df[year_df['金额'].abs() >= 1000]
        elif filter_type == 'small':
            year_df = year_df[year_df['金额'].abs() < 1000]

        available_years = sorted(df['交易时间'].dt.year.unique().tolist(), reverse=True)

        expense_df = year_df[
            (year_df['收/支'] == '支出') &
            (~year_df['是否退款'])
        ]
        income_df = year_df[
            (year_df['收/支'] == '收入') &
            (~year_df['是否退款'])
        ]

        yearly_stats = {
            'total_expense': round(expense_df['金额'].sum(), 2),
            'total_income': round(income_df['金额'].sum(), 2),
            'balance': round(income_df['金额'].sum() - expense_df['金额'].sum(), 2),
            'expense_count': len(expense_df),
            'income_count': len(income_df),
            'total_count': len(expense_df) + len(income_df),
            'active_days': len(year_df['日期'].unique()),
            'avg_transaction': round(expense_df['金额'].mean(), 2) if len(expense_df) > 0 else 0,
            'avg_daily_expense': round(expense_df['金额'].sum() / 365, 2),
            'avg_monthly_income': round(income_df['金额'].sum() / 12, 2),
            'expense_ratio': round(expense_df['金额'].sum() / income_df['金额'].sum() * 100, 2) if income_df['金额'].sum() > 0 else 0
        }

        all_months = [f'{year}-{str(month).zfill(2)}' for month in range(1, 13)]

        monthly_data = expense_df.groupby('月份')['金额'].sum().round(2)

        monthly_stats = pd.DataFrame(index=all_months)
        monthly_stats['total'] = monthly_data
        monthly_stats = monthly_stats.fillna(0)

        category_stats = expense_df.groupby('交易分类')['金额'].sum().round(2).sort_values(ascending=False)

        return jsonify({
            'available_years': available_years,
            'current_year': year,
            'yearly_stats': yearly_stats,
            'months': all_months,
            'amounts': monthly_stats['total'].tolist(),
            'categories': category_stats.index.tolist(),
            'amounts_by_category': category_stats.values.tolist()
        })

    except Exception as e:
        logger.error(f"API错误: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/monthly_data')
def get_monthly_data():
    """获取月度数据"""
    try:
        df = load_alipay_data()

        available_months = sorted(df['月份'].unique().tolist(), reverse=True)

        latest_month = available_months[0]
        default_year = int(latest_month.split('-')[0])
        default_month = int(latest_month.split('-')[1])

        current_year = request.args.get('year', default_year, type=int)
        current_month = request.args.get('month', default_month, type=int)

        logger.info(f"请求月度数据: {current_year}-{current_month}")

        current_month_str = f"{current_year}-{current_month:02d}"
        current_month_df = df[df['月份'] == current_month_str].copy()

        if current_month == 1:
            last_month_year = current_year - 1
            last_month = 12
        else:
            last_month_year = current_year
            last_month = current_month - 1

        last_month_str = f"{last_month_year}-{last_month:02d}"
        last_month_df = df[df['月份'] == last_month_str].copy()

        filter_type = request.args.get('filter', 'all')

        if filter_type == 'large':
            current_month_df = current_month_df[current_month_df['金额'] >= 1000]
            last_month_df = last_month_df[last_month_df['金额'] >= 1000] if not last_month_df.empty else last_month_df
        elif filter_type == 'small':
            current_month_df = current_month_df[current_month_df['金额'] < 1000]
            last_month_df = last_month_df[last_month_df['金额'] < 1000] if not last_month_df.empty else last_month_df

        current_stats = calculate_monthly_stats(current_month_df)
        monthly_stats = {
            **current_stats,
        }

        if not last_month_df.empty:
            last_stats = calculate_monthly_stats(last_month_df)

            comparisons = {}
            for key in ['total_expense', 'total_income', 'balance']:
                current_val = current_stats[key]
                last_val = last_stats[key]
                diff = current_val - last_val
                rate = (diff / abs(last_val) * 100) if last_val != 0 else 0
                comparisons[key] = {
                    'diff': diff,
                    'rate': rate
                }
            monthly_stats['comparisons'] = comparisons

        return jsonify({
            'success': True,
            'data': monthly_stats
        })

    except Exception as e:
        logger.error(f"Error in monthly analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/categories')
def get_categories():
    """获取所有交易分类"""
    try:
        df = load_alipay_data()
        categories = sorted(df['交易分类'].dropna().unique().tolist())
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/yearly_data')
def yearly_data():
    """获取年度数据"""
    try:
        df = load_alipay_data()
        logger.info(f"数据加载完成，总行数: {len(df)}")

        available_years = sorted(df['交易时间'].dt.year.unique().tolist(), reverse=True)

        year = request.args.get('year', available_years[0], type=int)
        logger.info(f"请求年度数据: {year}")

        current_year_df = df[df['交易时间'].dt.year == year].copy()
        logger.info(f"当前年份数据行数: {len(current_year_df)}")

        last_year_df = df[df['交易时间'].dt.year == (year - 1)].copy()
        logger.info(f"上一年数据行数: {len(last_year_df)}")

        filter_type = request.args.get('filter', 'all')

        if filter_type == 'large':
            current_year_df = current_year_df[current_year_df['金额'] >= 1000]
            last_year_df = last_year_df[last_year_df['金额'] >= 1000] if not last_year_df.empty else last_year_df
        elif filter_type == 'small':
            current_year_df = current_year_df[current_year_df['金额'] < 1000]
            last_year_df = last_year_df[last_year_df['金额'] < 1000] if not last_year_df.empty else last_year_df

        current_stats = calculate_yearly_stats(current_year_df)

        yearly_stats = {
            **current_stats,
        }

        if len(last_year_df) > 0:
            last_year_stats = calculate_yearly_stats(last_year_df)

            balance_change_rate = calculate_change_rate(current_stats['balance'], last_year_stats['balance'])
            expense_change_rate = calculate_change_rate(current_stats['total_expense'], last_year_stats['total_expense'])
            income_change_rate = calculate_change_rate(current_stats['total_income'], last_year_stats['total_income'])
            transaction_change_rate = calculate_change_rate(current_stats['total_count'], last_year_stats['total_count'])

            yearly_stats.update({
                'balance_change': float(current_stats['balance'] - last_year_stats['balance']),
                'expense_change': float(current_stats['total_expense'] - last_year_stats['total_expense']),
                'income_change': float(current_stats['total_income'] - last_year_stats['total_income']),
                'transaction_change': int(current_stats['total_count'] - last_year_stats['total_count']),
                'balance_change_rate': float(balance_change_rate) if balance_change_rate is not None else None,
                'expense_change_rate': float(expense_change_rate) if expense_change_rate is not None else None,
                'income_change_rate': float(income_change_rate) if income_change_rate is not None else None,
                'transaction_change_rate': float(transaction_change_rate) if transaction_change_rate is not None else None
            })
        else:
            yearly_stats.update({
                'balance_change': None,
                'expense_change': None,
                'income_change': None,
                'transaction_change': None,
                'balance_change_rate': None,
                'expense_change_rate': None,
                'income_change_rate': None,
                'transaction_change_rate': None
            })

        months = sorted(current_year_df['月份'].unique().tolist())
        expenses = []
        incomes = []

        for month in months:
            month_data = current_year_df[current_year_df['月份'] == month]
            expenses.append(float(round(month_data[
                (month_data['收/支'] == '支出') &
                (~month_data['是否退款'])
            ]['金额'].sum(), 2)))
            incomes.append(float(round(month_data[
                (month_data['收/支'] == '收入') &
                (~month_data['是否退款'])
            ]['金额'].sum(), 2)))

        expense_df = current_year_df[
            (current_year_df['收/支'] == '支出') &
            (~current_year_df['是否退款'])
        ]
        categories = expense_df.groupby('交易分类')['金额'].sum().sort_values(ascending=False)

        return jsonify({
            'yearly_stats': yearly_stats,
            'months': months,
            'expenses': expenses,
            'incomes': incomes,
            'categories': categories.index.tolist(),
            'amounts_by_category': [float(x) for x in categories.values.tolist()],
            'available_years': available_years,
            'current_year': int(year)
        })

    except Exception as e:
        logger.error(f"处理年度数据时出错: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/category_analysis')
def category_analysis():
    """分类分析 API"""
    try:
        df = load_alipay_data()
        category = request.args.get('category')
        time_range = request.args.get('range', 'year')
        year = request.args.get('year')
        month = request.args.get('month')
        min_amount = request.args.get('min_amount')
        max_amount = request.args.get('max_amount')

        expense_df = df[
            (df['收/支'] == '支出') &
            (~df['是否退款'])
        ]

        if time_range == 'year' and year:
            expense_df = expense_df[expense_df['交易时间'].dt.year == int(year)]
        elif time_range == 'month' and year and month:
            expense_df = expense_df[
                (expense_df['交易时间'].dt.year == int(year)) &
                (expense_df['交易时间'].dt.month == int(month))
            ]

        try:
            if min_amount:
                min_val = float(min_amount)
                expense_df = expense_df[expense_df['金额'] >= min_val]
            if max_amount and max_amount.lower() != 'infinity':
                max_val = float(max_amount)
                expense_df = expense_df[expense_df['金额'] < max_val]
        except ValueError as e:
            logger.warning(f"金额转换错误: {str(e)}")

        if not category:
            categories_stats = expense_df.groupby('交易分类').agg({
                '金额': ['sum', 'count', 'mean']
            }).round(2)

            categories_stats.columns = ['total', 'count', 'avg']

            categories_stats['amount_rank'] = categories_stats['total'].rank(ascending=False)
            categories_stats['count_rank'] = categories_stats['count'].rank(ascending=False)
            categories_stats['score'] = 0.7 * categories_stats['amount_rank'] + 0.3 * categories_stats['count_rank']

            categories_stats = categories_stats.sort_values('score', ascending=True)

            category_groups = None
            if '来源' in expense_df.columns:
                global_order = categories_stats['score'].sort_values(ascending=True).index.tolist()

                alipay_existing = expense_df[expense_df['来源'] == '支付宝']['交易分类'].unique()
                wechat_existing = expense_df[expense_df['来源'] == '微信']['交易分类'].unique()

                alipay_cats = [cat for cat in global_order if cat in alipay_existing]
                wechat_cats = [cat for cat in global_order if cat in wechat_existing]

                alipay_set = set(alipay_cats)
                wechat_cats = [c for c in wechat_cats if c not in alipay_set]

                category_groups = {
                    'alipay': alipay_cats,
                    'wechat': wechat_cats
                }

            return jsonify({
                'categories': categories_stats.index.tolist(),
                'category_groups': category_groups,
                'stats': {
                    'totals': categories_stats['total'].tolist(),
                    'counts': categories_stats['count'].tolist(),
                    'averages': categories_stats['avg'].tolist()
                }
            })

        category_df = expense_df[expense_df['交易分类'] == category]

        if category_df.empty:
            return jsonify({
                'error': f'未找到分类 "{category}" 的数据'
            }), 404

        if time_range == 'all':
            date_range = (category_df['交易时间'].max() - category_df['交易时间'].min()).days + 1
        elif time_range == 'year':
            date_range = 365
        else:
            date_range = calendar.monthrange(int(year), int(month))[1]

        total_expense = category_df['金额'].sum()
        transaction_count = len(category_df)
        avg_amount = round(category_df['金额'].mean(), 2) if transaction_count > 0 else 0

        if time_range == 'all':
            total_all_expense = expense_df['金额'].sum()
        elif time_range == 'year':
            total_all_expense = expense_df[expense_df['交易时间'].dt.year == int(year)]['金额'].sum()
        else:
            total_all_expense = expense_df[
                (expense_df['交易时间'].dt.year == int(year)) &
                (expense_df['交易时间'].dt.month == int(month))
            ]['金额'].sum()

        expense_ratio = round((total_expense / total_all_expense * 100), 2) if total_all_expense > 0 else 0

        if time_range == 'all':
            grouped = category_df.groupby(category_df['交易时间'].dt.strftime('%Y'))
            total_grouped = expense_df.groupby(expense_df['交易时间'].dt.strftime('%Y'))
        elif time_range == 'year':
            grouped = category_df.groupby(category_df['交易时间'].dt.strftime('%Y-%m'))
            total_grouped = expense_df.groupby(expense_df['交易时间'].dt.strftime('%Y-%m'))
        else:
            grouped = category_df.groupby(category_df['交易时间'].dt.strftime('%Y-%m-%d'))
            total_grouped = expense_df.groupby(expense_df['交易时间'].dt.strftime('%Y-%m-%d'))

        time_series = grouped['金额'].sum().round(2)
        total_series = total_grouped['金额'].sum().round(2)
        transaction_counts = grouped.size()

        ratios = []
        for date in time_series.index:
            if date in total_series.index and total_series[date] > 0:
                ratio = (time_series[date] / total_series[date] * 100).round(1)
            else:
                ratio = 0
            ratios.append(ratio)

        full_time_series = time_series.copy()
        full_transaction_counts = transaction_counts.copy()
        full_ratios = []

        if time_range == 'year':
            full_index = pd.period_range(start=f'{year}-01', end=f'{year}-12', freq='M').strftime('%Y-%m')
            full_time_series = time_series.reindex(full_index, fill_value=0)
            full_transaction_counts = transaction_counts.reindex(full_index, fill_value=0)
            full_total_series = total_series.reindex(full_index, fill_value=0)

            for date in full_time_series.index:
                if full_total_series[date] > 0:
                    ratio = (full_time_series[date] / full_total_series[date] * 100).round(1)
                else:
                    ratio = 0
                full_ratios.append(ratio)

        elif time_range == 'month':
            days_in_month = calendar.monthrange(int(year), int(month))[1]
            full_index = pd.period_range(start=f'{year}-{month}-01', periods=days_in_month, freq='D').strftime('%Y-%m-%d')
            full_time_series = time_series.reindex(full_index, fill_value=0)
            full_transaction_counts = transaction_counts.reindex(full_index, fill_value=0)
            full_total_series = total_series.reindex(full_index, fill_value=0)

            for date in full_time_series.index:
                if full_total_series[date] > 0:
                    ratio = (full_time_series[date] / full_total_series[date] * 100).round(1)
                else:
                    ratio = 0
                full_ratios.append(ratio)
        else:
            full_time_series = time_series
            full_transaction_counts = transaction_counts
            full_ratios = ratios

        hour_pattern = category_df.groupby(category_df['交易时间'].dt.hour)['金额'].agg([
            ('count', 'count'),
            ('sum', 'sum')
        ]).round(2)

        amount_ranges = [0, 50, 100, 200, 500, 1000, float('inf')]
        amount_labels = ['0-50', '50-100', '100-200', '200-500', '500-1000', '1000+']
        amount_dist = pd.cut(category_df['金额'], bins=amount_ranges, labels=amount_labels)
        amount_distribution = amount_dist.value_counts().sort_index()

        full_hours = pd.Index(range(24), name='交易时间')
        hour_pattern_full = hour_pattern.reindex(full_hours, fill_value=0)

        amount_distribution_full = amount_distribution.reindex(amount_labels, fill_value=0)

        return jsonify({
            'category': category,
            'stats': {
                'total_expense': float(total_expense),
                'transaction_count': int(transaction_count),
                'avg_amount': float(avg_amount),
                'expense_ratio': float(expense_ratio),
                'date_range': int(date_range),
                'max_amount': float(category_df['金额'].max()) if not category_df.empty else 0,
                'min_amount': float(category_df['金额'].min()) if not category_df.empty else 0,
                'median_amount': float(category_df['金额'].median()) if not category_df.empty else 0
            },
            'trend': {
                'dates': full_time_series.index.tolist(),
                'amounts': full_time_series.fillna(0).values.tolist(),
                'counts': full_transaction_counts.fillna(0).values.tolist(),
                'ratios': [0 if np.isnan(x) else x for x in full_ratios]
            },
            'pattern': {
                'hours': hour_pattern_full.index.tolist(),
                'counts': hour_pattern_full['count'].tolist(),
                'amounts': hour_pattern_full['sum'].tolist(),
                'averages': (hour_pattern_full['sum'] / hour_pattern_full['count']).round(2).fillna(0).tolist()
            },
            'distribution': {
                'ranges': amount_distribution_full.index.tolist(),
                'counts': amount_distribution_full.values.tolist(),
                'percentages': (amount_distribution_full / amount_distribution_full.sum() * 100).round(1).fillna(0).tolist()
            }
        })

    except Exception as e:
        logger.error(f"处理分类分析数据时出错: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/available_dates')
def get_available_dates():
    """获取可用的日期列表"""
    try:
        df = load_alipay_data()
        dates = df['交易时间'].dt.strftime('%Y-%m').unique().tolist()
        dates.sort(reverse=True)

        return jsonify({
            'success': True,
            'months': dates,
            'years': sorted(df['交易时间'].dt.year.unique().tolist(), reverse=True)
        })
    except Exception as e:
        logger.error(f"Error getting available dates: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/available_years')
def get_available_years():
    """获取数据中所有可用的年份"""
    try:
        df = load_alipay_data()
        years = sorted(df['交易时间'].dt.year.unique().tolist(), reverse=True)

        return jsonify({
            'success': True,
            'years': years
        })

    except Exception as e:
        logger.error(f"获取可用年份时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'获取可用年份失败: {str(e)}'
        }), 500


@app.route('/api/category_available_dates')
def get_category_available_dates():
    """获取分类页面的可用日期"""
    try:
        df = load_alipay_data()

        dates = pd.DataFrame({
            'year': df['交易时间'].dt.year,
            'month': df['交易时间'].dt.month
        })

        available_months = {}
        for year in sorted(dates['year'].unique(), reverse=True):
            months = sorted(dates[dates['year'] == year]['month'].unique())
            available_months[int(year)] = [int(m) for m in months]

        return jsonify({
            'years': sorted(dates['year'].unique().tolist(), reverse=True),
            'months': available_months
        })
    except Exception as e:
        logger.error(f"Error getting category available dates: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


# ============ 错误处理 ============

@app.errorhandler(404)
def not_found_error(error):
    return "页面未找到 - 404", 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({
        'success': False,
        'error': '服务器内部错误，请稍后重试'
    }), 500


# ============ 启动代码 ============

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host=HOST, port=PORT, debug=DEBUG)
