import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

// LocalStorage key
const FILTER_KEY = 'xiaoyao_transaction_filter'

// 筛选类型定义
export const FilterType = {
  ALL: 'all',      // 全部交易
  LARGE: 'large',  // 仅大额交易 (>= 1000元)
  SMALL: 'small'   // 仅小额交易 (< 1000元)
}

export const useFilterStore = defineStore('filter', () => {
  // 从 localStorage 恢复筛选状态
  const savedFilter = localStorage.getItem(FILTER_KEY) || FilterType.ALL

  // 当前筛选类型
  const currentFilter = ref(savedFilter)

  // 监听筛选变化，同步到 localStorage
  watch(currentFilter, (newValue) => {
    localStorage.setItem(FILTER_KEY, newValue)
    console.log('[Filter] Filter changed and saved:', newValue)
  })

  /**
   * 设置筛选类型
   */
  function setFilter(filterType) {
    if (Object.values(FilterType).includes(filterType)) {
      currentFilter.value = filterType
      console.log('[Filter] Filter set to:', filterType)
    } else {
      console.warn('[Filter] Invalid filter type:', filterType)
    }
  }

  /**
   * 获取当前筛选类型
   */
  function getFilter() {
    return currentFilter.value
  }

  /**
   * 检查是否显示该交易
   * @param {number} amount - 交易金额
   * @returns {boolean} 是否显示
   */
  function shouldShowTransaction(amount) {
    switch (currentFilter.value) {
      case FilterType.LARGE:
        return amount >= 1000
      case FilterType.SMALL:
        return amount < 1000
      case FilterType.ALL:
      default:
        return true
    }
  }

  /**
   * 获取筛选参数（用于 API 请求）
   * @returns {Object} 筛选参数
   */
  function getFilterParams() {
    console.log('[Filter] Getting filter params for:', currentFilter.value)
    const params = {
      [FilterType.LARGE]: { min_amount: 1000 },
      [FilterType.SMALL]: { max_amount: 1000 },
      [FilterType.ALL]: {}
    }
    const result = params[currentFilter.value] || {}
    console.log('[Filter] Returning filter params:', result)
    return result
  }

  /**
   * 获取筛选显示名称
   */
  function getFilterLabel() {
    switch (currentFilter.value) {
      case FilterType.LARGE:
        return '仅大额交易'
      case FilterType.SMALL:
        return '仅小额交易'
      case FilterType.ALL:
      default:
        return '全部交易'
    }
  }

  return {
    currentFilter,
    setFilter,
    getFilter,
    shouldShowTransaction,
    getFilterParams,
    getFilterLabel
  }
})
