import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'

export const useDataStore = defineStore('data', () => {
  // 状态
  const yearlyData = ref(null)
  const monthlyData = ref(null)
  const categoryData = ref(null)
  const transactions = ref([])
  const availableYears = ref([])
  const availableDates = ref([])
  const categories = ref([])

  // 筛选条件
  const filters = ref({
    year: null,
    month: null,
    category: null,
    amountRange: null
  })

  // ==================== 数据加载 ====================

  /**
   * 加载年度数据
   */
  async function loadYearlyData(params = {}) {
    try {
      console.log('[DataStore] Calling getYearlyAnalysis with params:', params)
      const result = await api.getYearlyAnalysis(params)
      console.log('[DataStore] getYearlyAnalysis result:', result)
      yearlyData.value = result
      return yearlyData.value
    } catch (error) {
      console.error('[DataStore] 加载年度数据失败:', error)
      throw error
    }
  }

  /**
   * 加载月度数据
   */
  async function loadMonthlyData(params = {}) {
    try {
      monthlyData.value = await api.getMonthlyAnalysis(params)
      return monthlyData.value
    } catch (error) {
      console.error('加载月度数据失败:', error)
      throw error
    }
  }

  /**
   * 加载分类数据
   */
  async function loadCategoryData(params = {}) {
    try {
      categoryData.value = await api.getCategoryExpenses(params)
      return categoryData.value
    } catch (error) {
      console.error('加载分类数据失败:', error)
      throw error
    }
  }

  /**
   * 加载交易记录
   */
  async function loadTransactions(params = {}) {
    try {
      const result = await api.getTransactions(params)
      transactions.value = result.transactions || []
      return result
    } catch (error) {
      console.error('加载交易记录失败:', error)
      throw error
    }
  }

  /**
   * 加载可用年份
   */
  async function loadAvailableYears() {
    try {
      console.log('[DataStore] Loading available years...')
      const result = await api.getAvailableYears()
      console.log('[DataStore] API result:', result)

      // 处理不同的响应格式
      // 可能是 { years: [...] } 或直接的数组 [...]
      const years = Array.isArray(result) ? result : (result.years || [])
      console.log('[DataStore] Available years:', years)

      availableYears.value = years
      return availableYears.value
    } catch (error) {
      console.error('[DataStore] 加载可用年份失败:', error)
      return []
    }
  }

  /**
   * 加载可用日期
   */
  async function loadAvailableDates() {
    try {
      availableDates.value = await api.getAvailableDates()
      return availableDates.value
    } catch (error) {
      console.error('加载可用日期失败:', error)
      return []
    }
  }

  /**
   * 加载分类列表
   */
  async function loadCategories() {
    try {
      categories.value = await api.getCategories()
      return categories.value
    } catch (error) {
      console.error('加载分类失败:', error)
      return []
    }
  }

  // ==================== 筛选条件 ====================

  function setFilter(key, value) {
    filters.value[key] = value
  }

  function resetFilters() {
    filters.value = {
      year: null,
      month: null,
      category: null,
      amountRange: null
    }
  }

  return {
    // 状态
    yearlyData,
    monthlyData,
    categoryData,
    transactions,
    availableYears,
    availableDates,
    categories,
    filters,

    // 方法
    loadYearlyData,
    loadMonthlyData,
    loadCategoryData,
    loadTransactions,
    loadAvailableYears,
    loadAvailableDates,
    loadCategories,
    setFilter,
    resetFilters
  }
})
