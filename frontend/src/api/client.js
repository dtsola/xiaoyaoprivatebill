// API 基础配置
const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * 统一 API 客户端
 * 复用现有后端 API，零修改后端代码
 */
export const api = {
  // ==================== 数据分析 API ====================
  /**
   * 获取年度分析数据
   * @param {Object} params - 查询参数 { year, min_amount, max_amount }
   */
  getYearlyAnalysis: (params) => get('/yearly_analysis', params),

  /**
   * 获取月度分析数据
   * @param {Object} params - 查询参数 { year, month }
   */
  getMonthlyAnalysis: (params) => get('/monthly_analysis', params),

  /**
   * 获取分类支出数据
   * @param {Object} params - 查询参数 { year, month }
   */
  getCategoryExpenses: (params) => get('/category_expenses', params),

  /**
   * 获取交易记录列表
   * @param {Object} params - 查询参数 { page, per_page, year, month, category, type, min_amount, max_amount, search }
   */
  getTransactions: (params) => get('/transactions', params),

  /**
   * 获取综合分析数据
   * @param {Object} params - 查询参数 { year }
   */
  getAnalysis: (params) => get('/analysis', params),

  /**
   * 获取时间分析数据
   * @param {Object} params - 查询参数 { year }
   */
  getTimeAnalysis: (params) => get('/time_analysis', params),

  /**
   * 获取汇总数据
   */
  getSummary: () => get('/summary'),

  // ==================== 元数据 API ====================
  /**
   * 获取可用日期列表
   */
  getAvailableDates: () => get('/available_dates'),

  /**
   * 获取可用年份列表
   */
  getAvailableYears: () => get('/available_years'),

  /**
   * 获取所有分类
   */
  getCategories: () => get('/categories'),

  // ==================== 文件管理 API ====================
  /**
   * 上传文件
   * @param {FormData} formData - 文件数据
   */
  uploadFile: (formData) => post('/upload', formData),

  /**
   * 获取已上传文件列表
   */
  getFiles: () => get('/files'),

  /**
   * 删除文件
   * @param {string} filename - 文件名
   */
  deleteFile: (filename) => delete_(`/files/${filename}`),

  /**
   * 清除所有数据
   */
  clearData: () => post('/clear_data'),

  // ==================== 会话管理 API ====================
  /**
   * 进入演示模式
   */
  enterDemo: () => post('/demo/enter'),

  /**
   * 退出演示模式
   */
  exitDemo: () => post('/demo/exit'),

  /**
   * 获取会话状态 (特殊处理 - 后端返回格式不同)
   */
  getSessionStatus: () => getSessionStatus(),

  /**
   * 获取会话剩余时间
   */
  getTimeRemaining: () => get('/session/time_remaining')
}

// ==================== 请求封装函数 ====================

/**
 * GET 请求
 * @param {string} endpoint - API 端点
 * @param {Object} params - 查询参数
 */
async function get(endpoint, params) {
  const url = new URL(API_BASE + endpoint, window.location.origin)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, String(value))
      }
    })
  }

  console.log('[API] GET request to:', url.toString())

  const response = await fetch(url)
  const data = await response.json()

  console.log('[API] Response:', data)

  if (!data.success) {
    throw new Error(data.error || '请求失败')
  }

  // 处理不同的响应格式
  // 有些端点返回 { success: true, data: {...} }
  // 有些端点返回 { success: true, years: [...] } 或其他直接数据
  if ('data' in data) {
    return data.data
  }

  // 如果没有 data 字段，返回整个响应对象（去掉 success 字段）
  const { success, ...result } = data
  return result
}

/**
 * POST 请求
 * @param {string} endpoint - API 端点
 * @param {Object|FormData} data - 请求数据
 */
async function post(endpoint, data) {
  const isFormData = data instanceof FormData

  const response = await fetch(API_BASE + endpoint, {
    method: 'POST',
    headers: isFormData ? {} : { 'Content-Type': 'application/json' },
    body: isFormData ? data : JSON.stringify(data)
  })

  const result = await response.json()

  if (!result.success) {
    throw new Error(result.error || '请求失败')
  }

  // 处理不同的响应格式
  if ('data' in result) {
    return result.data
  }

  // 如果没有 data 字段，返回整个响应对象（去掉 success 字段）
  const { success, ...responseData } = result
  return responseData
}

/**
 * DELETE 请求
 * @param {string} endpoint - API 端点
 */
async function delete_(endpoint) {
  const response = await fetch(API_BASE + endpoint, {
    method: 'DELETE'
  })

  const data = await response.json()

  if (!data.success) {
    throw new Error(data.error || '请求失败')
  }

  // 处理不同的响应格式
  if ('data' in data) {
    return data.data
  }

  // 如果没有 data 字段，返回整个响应对象（去掉 success 字段）
  const { success, ...result } = data
  return result
}

/**
 * 获取会话状态 (特殊处理)
 * 后端返回格式: { active: boolean, message: string }
 * 而不是标准的 { success: boolean, data: {...} }
 */
async function getSessionStatus() {
  console.log('[API] Getting session status...')
  try {
    const response = await fetch(API_BASE + '/session/status')
    const data = await response.json()
    console.log('[API] Session status response:', data)

    // 后端返回格式: { active: boolean, message: string }
    // 我们需要转换为前端期望的格式
    // 注意: 后端的 session/status 不返回 is_demo 字段
    // 所以我们需要通过其他方式判断演示模式
    return {
      active: data.active || false,
      message: data.message || '',
      // 由于后端不返回 is_demo，我们需要在客户端维护这个状态
      is_demo: false  // 这个值会在 session store 中被覆盖
    }
  } catch (error) {
    console.error('[API] Session status error:', error)
    // 出错时返回默认状态
    return {
      active: false,
      message: '获取会话状态失败',
      is_demo: false
    }
  }
}

export default api
