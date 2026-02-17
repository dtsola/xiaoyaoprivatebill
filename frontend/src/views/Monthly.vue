<template>
  <div class="monthly-page">
    <div class="page-header">
      <h1 class="page-title">月度分析</h1>
      <div class="header-actions">
        <select v-model="filters.year" @change="loadData" class="filter-select">
          <option value="">选择年份</option>
          <option v-for="year in dataStore.availableYears" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
        <select v-model="filters.month" @change="loadData" class="filter-select">
          <option value="">选择月份</option>
          <option v-for="month in availableMonths" :key="month" :value="month">
            {{ month }}月
          </option>
        </select>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !monthlyData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="monthlyData" class="monthly-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <StatCard
          title="本月支出"
          :value="formatMoney(monthlyData.stats?.balance?.expense || 0)"
          :change="monthlyData.stats?.balance?.expense_change"
          icon="fas fa-shopping-cart"
          color="#FF3B30"
        />
        <StatCard
          title="本月收入"
          :value="formatMoney(monthlyData.stats?.balance?.income || 0)"
          :change="monthlyData.stats?.balance?.income_change"
          icon="fas fa-wallet"
          color="#34C759"
        />
        <StatCard
          title="本月结余"
          :value="formatMoney(monthlyData.stats?.balance?.balance || 0)"
          icon="fas fa-piggy-bank"
          color="#007AFF"
        />
        <StatCard
          title="交易笔数"
          :value="monthlyData.stats?.transaction_count || 0"
          icon="fas fa-receipt"
          color="#FF9500"
        />
      </div>

      <!-- 图表区域 -->
      <div class="charts-container">
        <!-- 每日支出趋势 -->
        <div class="chart-card full-width">
          <div class="chart-header">
            <h3 class="chart-title">每日支出趋势</h3>
          </div>
          <div ref="dailyTrendChartRef" class="chart-body"></div>
        </div>

        <!-- 分类支出 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">分类支出</h3>
          </div>
          <div ref="categoryChartRef" class="chart-body"></div>
        </div>

        <!-- 收支构成 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">收支构成</h3>
          </div>
          <div ref="compositionChartRef" class="chart-body"></div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <i class="fas fa-calendar-alt empty-icon"></i>
      <p>请选择年份和月份查看分析</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import StatCard from '@/components/common/StatCard.vue'
import { formatMoney } from '@/utils/format'
import * as echarts from 'echarts'

const dataStore = useDataStore()
const uiStore = useUiStore()

const filters = ref({
  year: null,
  month: null
})

const monthlyData = ref(null)
const availableMonths = computed(() => {
  const months = []
  for (let i = 1; i <= 12; i++) {
    months.push(i)
  }
  return months
})

// 图表引用
const dailyTrendChartRef = ref(null)
const categoryChartRef = ref(null)
const compositionChartRef = ref(null)

// 图表实例
let dailyTrendChart = null
let categoryChart = null
let compositionChart = null

async function loadData() {
  if (!filters.value.year) {
    monthlyData.value = null
    return
  }

  try {
    uiStore.setGlobalLoading(true)
    const params = { year: filters.value.year }
    if (filters.value.month) {
      params.month = filters.value.month
    }
    monthlyData.value = await dataStore.loadMonthlyData(params)

    await nextTick()
    initCharts()
  } catch (error) {
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function initCharts() {
  initDailyTrendChart()
  initCategoryChart()
  initCompositionChart()
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  dailyTrendChart?.resize()
  categoryChart?.resize()
  compositionChart?.resize()
}

function initDailyTrendChart() {
  if (!dailyTrendChartRef.value) return

  dailyTrendChart = echarts.init(dailyTrendChartRef.value)

  const dailyData = monthlyData.value?.daily_data?.expense || {}
  const dates = Object.keys(dailyData).sort()
  const values = dates.map(d => dailyData[d])

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>支出: ¥${param.value.toLocaleString()}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '支出',
      type: 'bar',
      data: values,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#007AFF' },
          { offset: 1, color: '#5856D6' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }

  dailyTrendChart.setOption(option)
}

function initCategoryChart() {
  if (!categoryChartRef.value) return

  categoryChart = echarts.init(categoryChartRef.value)

  const categoryData = monthlyData.value?.categories?.expense || {}
  const categories = Object.keys(categoryData).sort((a, b) => categoryData[b] - categoryData[a])
  const values = categories.map(c => categoryData[c])

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>¥${param.value.toLocaleString()}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: categories
    },
    series: [{
      type: 'bar',
      data: values,
      itemStyle: {
        color: (params) => {
          const colors = ['#FF3B30', '#FF9500', '#FFCC00', '#34C759', '#30B0C7', '#007AFF', '#5856D6', '#AF52DE']
          return colors[params.dataIndex % colors.length]
        },
        borderRadius: [0, 4, 4, 0]
      }
    }]
  }

  categoryChart.setOption(option)
}

function initCompositionChart() {
  if (!compositionChartRef.value) return

  compositionChart = echarts.init(compositionChartRef.value)

  const incomeByCategory = monthlyData.value?.categories?.income || {}
  const expenseByCategory = monthlyData.value?.categories?.expense || {}

  const categories = [...new Set([...Object.keys(incomeByCategory), ...Object.keys(expenseByCategory)])]

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['收入', '支出'],
      top: '5%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories.slice(0, 10)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '收入',
        type: 'bar',
        data: categories.slice(0, 10).map(c => incomeByCategory[c] || 0),
        itemStyle: {
          color: '#34C759'
        }
      },
      {
        name: '支出',
        type: 'bar',
        data: categories.slice(0, 10).map(c => expenseByCategory[c] || 0),
        itemStyle: {
          color: '#FF3B30'
        }
      }
    ]
  }

  compositionChart.setOption(option)
}

onMounted(async () => {
  await dataStore.loadAvailableYears()
  // 默认选择当前年份
  const currentYear = new Date().getFullYear()
  if (dataStore.availableYears.includes(currentYear)) {
    filters.value.year = currentYear
    await loadData()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  dailyTrendChart?.dispose()
  categoryChart?.dispose()
  compositionChart?.dispose()
})
</script>

<style scoped>
.monthly-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  color: var(--text-color);
  font-size: 14px;
  cursor: pointer;
}

.page-loading,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: var(--secondary-text);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-card {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-card);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.chart-body {
  height: 320px;
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
