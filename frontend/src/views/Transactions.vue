<template>
  <div class="transactions-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">交易记录</h1>
    </div>

    <!-- 卡片容器 -->
    <div class="card">
      <!-- 表格头部和筛选器 -->
      <div class="table-header">
        <h3>交易明细</h3>
        <div class="table-filters">
          <select v-model="filters.month" @change="onFilterChange" class="filter-select">
            <option value="">全部时间</option>
            <option v-for="month in availableMonths" :key="month" :value="month">
              {{ month }}
            </option>
          </select>
          <select v-model="filters.category" @change="onFilterChange" class="filter-select">
            <option value="">全部分类</option>
            <option v-for="cat in categories" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
          <select v-model="filters.type" @change="onFilterChange" class="filter-select">
            <option value="">全部类型</option>
            <option value="收入">收入</option>
            <option value="支出">支出</option>
          </select>
          <input
            v-model="filters.search"
            type="text"
            placeholder="搜索交易..."
            class="filter-input"
            @keyup.enter="onFilterChange"
          />
        </div>
      </div>

      <!-- 表格容器 -->
      <div class="table-container">
        <div v-if="uiStore.globalLoading" class="table-loading">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="transactions.length === 0" class="empty-state">
          <i class="fas fa-receipt empty-icon"></i>
          <p>暂无交易记录</p>
        </div>

        <table v-else id="transactionTable" class="transaction-table">
          <thead>
            <tr>
              <th>交易时间</th>
              <th>商品说明</th>
              <th>交易对方</th>
              <th>分类</th>
              <th>收/支</th>
              <th>金额</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in transactions" :key="tx.time + tx.description" class="table-row">
              <td>{{ tx.time }}</td>
              <td :title="tx.description">{{ tx.description }}</td>
              <td :title="tx.counterparty || ''">{{ tx.counterparty || '-' }}</td>
              <td>{{ tx.category }}</td>
              <td>{{ tx.type }}</td>
              <td :class="['amount', tx.type === '收入' ? 'income' : 'expense']">
                {{ parseFloat(tx.amount).toFixed(2) }}
              </td>
              <td>
                <span :class="['status-tag', tx.status === '交易成功' ? 'success' : 'refund']">
                  {{ tx.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="table-pagination">
        <button
          class="pagination-btn"
          :disabled="pagination.current_page <= 1"
          @click="goToPage(pagination.current_page - 1)"
        >
          上一页
        </button>
        <span id="pageInfo" class="page-info">
          第 {{ pagination.current_page }} 页 / 共 {{ pagination.total_pages }} 页 ({{ pagination.total_records }} 条记录)
        </span>
        <button
          class="pagination-btn"
          :disabled="pagination.current_page >= pagination.total_pages"
          @click="goToPage(pagination.current_page + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import { useSessionStore } from '@/stores/session'
import { useFilterStore } from '@/stores/filter'
import api from '@/api/client'

const dataStore = useDataStore()
const uiStore = useUiStore()
const sessionStore = useSessionStore()
const filterStore = useFilterStore()

const transactions = ref([])
const availableMonths = ref([])
const categories = ref([])

const pagination = reactive({
  current_page: 1,
  per_page: 20,
  total_pages: 1,
  total_records: 0
})

const filters = reactive({
  month: '',
  category: '',
  type: '',
  search: ''
})

// 搜索防抖定时器
let searchTimeout = null

// 加载可用月份（从 available_dates API）
async function loadAvailableMonths() {
  try {
    const data = await api.getAvailableDates()
    console.log('[Transactions] Available months response:', data)

    if (data.months && data.months.length > 0) {
      availableMonths.value = data.months
      console.log('[Transactions] Loaded months:', availableMonths.value)
    } else {
      console.warn('[Transactions] No months found')
    }
  } catch (error) {
    console.error('[Transactions] 加载月份失败:', error)
  }
}

// 加载分类
async function loadCategories() {
  try {
    const data = await api.getCategories()
    console.log('[Transactions] Categories response:', data)

    // API 客户端会移除 success 字段，直接返回 { categories: [...] }
    if (data.categories && data.categories.length > 0) {
      categories.value = data.categories
      console.log('[Transactions] Loaded categories:', categories.value)
    } else {
      console.warn('[Transactions] No categories found')
    }
  } catch (error) {
    console.error('[Transactions] 加载分类失败:', error)
  }
}

// 解析月份筛选器值
function parseMonthFilter(monthValue) {
  if (!monthValue) return { year: '', month: '' }

  const parts = monthValue.split('-')
  if (parts.length === 2) {
    return { year: parts[0], month: parts[1] }
  }
  return { year: '', month: '' }
}

// 加载交易记录
async function loadTransactions() {
  try {
    uiStore.setGlobalLoading(true)

    const { year, month } = parseMonthFilter(filters.month)

    // 构建参数，需要转换类型
    const params = {
      page: pagination.current_page,
      per_page: pagination.per_page
    }

    // 只有当值存在时才添加参数
    if (year) params.year = parseInt(year)
    if (month) params.month = parseInt(month)
    if (filters.category) params.category = filters.category
    if (filters.type) params.type = filters.type
    if (filters.search) params.search = filters.search

    // 添加金额筛选参数
    const filterParams = filterStore.getFilterParams()
    Object.assign(params, filterParams)

    console.log('[Transactions] Loading with params:', params)

    const data = await api.getTransactions(params)

    console.log('[Transactions] Received data:', data)

    transactions.value = data.transactions || []
    pagination.current_page = data.pagination?.current_page || 1
    pagination.total_pages = data.pagination?.total_pages || 1
    pagination.total_records = data.pagination?.total_records || 0

    console.log('[Transactions] Loaded', transactions.value.length, 'transactions')
  } catch (error) {
    console.error('[Transactions] Error:', error)
    uiStore.showError('加载交易记录失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

// 筛选器变化时重新加载（重置到第一页）
function onFilterChange() {
  pagination.current_page = 1
  loadTransactions()
}

// 跳转到指定页码
function goToPage(page) {
  if (page >= 1 && page <= pagination.total_pages) {
    pagination.current_page = page
    loadTransactions()
  }
}

// 初始化
onMounted(async () => {
  console.log('[Transactions] Component mounted')

  await loadAvailableMonths()
  await loadCategories()
  await loadTransactions()

  console.log('[Transactions] Initial load complete')
})

// 监听全局筛选器变化
watch(() => filterStore.currentFilter, (newFilter, oldFilter) => {
  console.log('[Transactions] Filter changed from', oldFilter, 'to', newFilter)
  // 重置到第一页并重新加载数据
  pagination.current_page = 1
  loadTransactions()
})
</script>

<style scoped>
.transactions-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 页面标题 */
.page-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--bg-color);
  margin: -20px -20px 24px -20px;
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: saturate(180%) blur(20px);
  background-color: rgba(245, 245, 247, 0.8);
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

/* 卡片容器 */
.card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-card);
}

/* 表格头部 */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color);
  margin: 0;
}

/* 筛选器 */
.table-filters {
  display: flex;
  gap: 12px;
}

.filter-select,
.filter-input {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: var(--hover-bg);
  color: var(--text-color);
  font-size: 13px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
}

.filter-select {
  padding-right: 32px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 8.825L1.175 4 2.238 2.938 6 6.7l3.763-3.763L10.825 4z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  cursor: pointer;
  /* 移除原生下拉箭头 */
  -webkit-appearance: none;
  appearance: none;
}

.filter-input {
  width: 200px;
}

.filter-select:hover,
.filter-input:hover {
  background-color: var(--border-color);
}

.filter-select:focus,
.filter-input:focus {
  background-color: white;
  box-shadow: 0 0 0 2px var(--primary-color);
}

/* 表格容器 */
.table-container {
  overflow-x: auto;
  border-radius: 12px;
  background: white;
}

.transaction-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.transaction-table th,
.transaction-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  white-space: nowrap;
}

.transaction-table th {
  background: var(--bg-color);
  color: var(--secondary-text);
  font-weight: normal;
  position: sticky;
  top: 0;
  z-index: 1;
}

.transaction-table tbody tr {
  transition: background-color 0.2s;
}

.transaction-table tbody tr:hover {
  background: var(--hover-bg);
}

/* 限制商品说明列宽 */
.transaction-table td:nth-child(2) {
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 限制交易对方列宽 */
.transaction-table td:nth-child(3) {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 金额样式 */
.amount {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Mono', monospace;
  text-align: right;
}

.amount.income {
  color: #34C759;
}

.amount.expense {
  color: #FF3B30;
}

/* 状态标签 */
.status-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.success {
  background: #E4FBE6;
  color: #34C759;
}

.status-tag.refund {
  background: #FFE5E5;
  color: #FF3B30;
}

/* 分页 */
.table-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 24px;
  gap: 16px;
}

.pagination-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: var(--hover-bg);
  color: var(--text-color);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.pagination-btn:not(:disabled):hover {
  background: var(--primary-color);
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: var(--secondary-text);
}

/* 加载和空状态 */
.table-loading,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--secondary-text);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}
</style>
