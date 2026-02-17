<template>
  <div class="transactions-page">
    <div class="page-header">
      <h1 class="page-title">交易记录</h1>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-bar">
      <select v-model="filters.year" @change="loadTransactions" class="filter-select">
        <option value="">全部年份</option>
        <option v-for="year in dataStore.availableYears" :key="year" :value="year">
          {{ year }}年
        </option>
      </select>

      <select v-model="filters.category" @change="loadTransactions" class="filter-select">
        <option value="">全部分类</option>
        <option v-for="cat in dataStore.categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <select v-model="filters.type" @change="loadTransactions" class="filter-select">
        <option value="">全部类型</option>
        <option value="支出">支出</option>
        <option value="收入">收入</option>
      </select>

      <input
        v-model="filters.search"
        type="text"
        placeholder="搜索交易描述..."
        class="filter-input"
        @keyup.enter="loadTransactions"
      />

      <button class="btn btn-primary" @click="loadTransactions">
        <i class="fas fa-search"></i>
        搜索
      </button>
    </div>

    <!-- 数据表格 -->
    <div class="table-container">
      <div v-if="uiStore.globalLoading" class="table-loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="transactions.length === 0" class="empty-state">
        <i class="fas fa-receipt empty-icon"></i>
        <p>暂无交易记录</p>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>交易时间</th>
            <th>描述</th>
            <th>分类</th>
            <th>类型</th>
            <th>金额</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.time + tx.description" class="table-row">
            <td>{{ formatDateTime(tx.time, 'datetime') }}</td>
            <td class="td-description">{{ tx.description }}</td>
            <td>{{ tx.category }}</td>
            <td>
              <span :class="['type-badge', tx.type === '支出' ? 'expense' : 'income']">
                {{ tx.type }}
              </span>
            </td>
            <td :class="['td-amount', tx.type === '支出' ? 'expense' : 'income']">
              {{ tx.type === '支出' ? '-' : '+' }}{{ formatMoney(tx.amount) }}
            </td>
            <td>{{ tx.status || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div v-if="pagination.total_pages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="pagination.current_page === 1"
        @click="goToPage(pagination.current_page - 1)"
      >
        上一页
      </button>
      <span class="page-info">第 {{ pagination.current_page }} / {{ pagination.total_pages }} 页</span>
      <button
        class="page-btn"
        :disabled="pagination.current_page === pagination.total_pages"
        @click="goToPage(pagination.current_page + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import { formatMoney, formatDateTime } from '@/utils/format'

const dataStore = useDataStore()
const uiStore = useUiStore()

const transactions = ref([])
const pagination = reactive({
  current_page: 1,
  per_page: 50,
  total_pages: 1,
  total_records: 0
})

const filters = reactive({
  year: '',
  month: '',
  category: '',
  type: '',
  search: ''
})

async function loadTransactions() {
  try {
    uiStore.setGlobalLoading(true)
    const params = {
      page: pagination.current_page,
      per_page: pagination.per_page,
      ...filters
    }
    const result = await dataStore.loadTransactions(params)
    transactions.value = result.transactions || []
    pagination.current_page = result.pagination?.current_page || 1
    pagination.total_pages = result.pagination?.total_pages || 1
    pagination.total_records = result.pagination?.total_records || 0
  } catch (error) {
    uiStore.showError('加载交易记录失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function goToPage(page) {
  pagination.current_page = page
  loadTransactions()
}

onMounted(async () => {
  await dataStore.loadAvailableYears()
  await dataStore.loadCategories()
  await loadTransactions()
})
</script>

<style scoped>
.transactions-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.filter-select,
.filter-input {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  color: var(--text-color);
  font-size: 14px;
}

.filter-select {
  min-width: 120px;
}

.filter-input {
  flex: 1;
  min-width: 200px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: #0066E6;
}

.table-container {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

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

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: var(--secondary-text);
  font-size: 13px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-color);
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  font-size: 14px;
  color: var(--text-color);
}

.table-row:hover {
  background: var(--hover-bg);
}

.td-description {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.type-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
}

.type-badge.expense {
  background: rgba(255, 59, 48, 0.1);
  color: var(--danger-color);
}

.type-badge.income {
  background: rgba(52, 199, 89, 0.1);
  color: var(--success-color);
}

.td-amount {
  font-weight: 600;
  font-family: var(--font-family-mono);
}

.td-amount.expense {
  color: var(--danger-color);
}

.td-amount.income {
  color: var(--success-color);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  margin-top: 20px;
  box-shadow: var(--shadow-card);
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--hover-bg);
  border-color: var(--primary-color);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: var(--secondary-text);
}
</style>
