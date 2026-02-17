/**
 * 格式化工具函数
 * 从 olds/static/js/utils.js 迁移
 */

// 分类颜色映射 (与后端保持一致)
export const CATEGORY_COLORS = {
  // 主要消费类别
  '餐饮美食': '#FF3B30',
  '酒店旅游': '#5856D6',
  '交通出行': '#007AFF',
  '服饰装扮': '#FF9500',
  '日用百货': '#34C759',
  '数码电器': '#32ADE6',

  // 生活服务类
  '生活服务': '#FF2D55',
  '爱车养车': '#AF52DE',
  '运动户外': '#FFD60A',

  // 文教娱乐类
  '文化休闲': '#FF6B22',
  '教育培训': '#64D2FF',

  // 居家类
  '家居家装': '#BF5AF2',
  '住房物业': '#AC8E68',

  // 其他服务类
  '医疗健康': '#30B0C7',
  '充值缴费': '#66D4CF',
  '公共服务': '#A7C538',
  '商业服务': '#5E5CE6',
  '信用借还': '#FF6482',
  '母婴亲子': '#40C8E0',

  // 添加收入分类颜色
  '收入': '#34C759',
  '转账红包': '#FF9500',
  '保险': '#007AFF',
  '其他': '#FF3B30',

  // 微信账单特定分类
  '商户消费': '#FF453A',
  '扫二维码付款': '#0A84FF',
  '转账': '#FF9F0A',
  '微信红包（单发）': '#FF375F',
  '微信红包（群红包）': '#FF375F',
  '微信红包': '#FF375F',
  '群收款': '#BF5AF2',

  // 默认类别
  '其他': '#8E8E93'
}

/**
 * 获取分类颜色
 */
export function getCategoryColor(category) {
  return CATEGORY_COLORS[category] || CATEGORY_COLORS['其他']
}

/**
 * 格式化金额
 * @param {number} value - 金额值
 * @returns {string} 格式化后的金额
 */
export function formatMoney(value) {
  return new Intl.NumberFormat('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

/**
 * 格式化时间范围
 * @param {number} seconds - 秒数
 * @returns {string} 格式化后的时间范围
 */
export function formatTime(seconds) {
  if (!seconds || seconds < 0) return '0秒'

  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  const parts = []
  if (hours > 0) parts.push(`${hours}小时`)
  if (minutes > 0) parts.push(`${minutes}分钟`)
  if (secs > 0 || parts.length === 0) parts.push(`${secs}秒`)

  return parts.join('')
}

/**
 * 格式化日期时间
 * @param {string|Date} date - 日期
 * @param {string} format - 格式类型
 * @returns {string} 格式化后的日期
 */
export function formatDateTime(date, format = 'datetime') {
  if (!date) return '-'

  const d = typeof date === 'string' ? new Date(date) : date

  if (isNaN(d.getTime())) return '-'

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')

  switch (format) {
    case 'date':
      return `${year}-${month}-${day}`
    case 'time':
      return `${hours}:${minutes}`
    case 'datetime':
    default:
      return `${year}-${month}-${day} ${hours}:${minutes}`
  }
}

/**
 * 计算变化率并返回显示文本
 * @param {number} current - 当前值
 * @param {number} previous - 之前值
 * @returns {Object} 包含变化值、变化率和显示文本
 */
export function calculateChange(current, previous) {
  if (previous === 0 || previous === null || previous === undefined) {
    return {
      change: current,
      changeRate: null,
      text: '暂无对比数据',
      trend: 'neutral'
    }
  }

  const change = current - previous
  const changeRate = ((change / Math.abs(previous)) * 100).toFixed(1)

  let trend = 'neutral'
  if (change > 0) trend = 'up'
  else if (change < 0) trend = 'down'

  const sign = change > 0 ? '+' : ''
  const text = `${sign}${formatMoney(change)} (${changeRate}%)`

  return { change, changeRate, text, trend }
}

export default {
  CATEGORY_COLORS,
  getCategoryColor,
  formatMoney,
  formatTime,
  formatDateTime,
  calculateChange
}
