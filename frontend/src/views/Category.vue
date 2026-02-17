<template>
  <div class="category-page">
    <div class="page-header">
      <h1 class="page-title">分类分析</h1>
      <div class="header-actions">
        <select v-model="filters.year" @change="loadData" class="filter-select">
          <option value="">选择年份</option>
          <option v-for="year in dataStore.availableYears" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
        <select v-model="filters.category" @change="loadData" class="filter-select">
          <option value="">选择分类</option>
          <option v-for="cat in dataStore.categories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !categoryData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="categoryData" class="category-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <StatCard
          title="分类总支出"
          :value="formatMoney(categoryData.stats?.total || 0)"
          :icon="getCategoryIcon(filters.category)"
          :color="getCategoryColor(filters.category)"
        />
        <StatCard
          title="交易笔数"
          :value="categoryData.stats?.count || 0"
          icon="fas fa-receipt"
          color="#007AFF"
        />
        <StatCard
          title="平均每笔"
          :value="formatMoney(categoryData.stats?.average || 0)"
          icon="fas fa-calculator"
          color="#FF9500"
        />
        <StatCard
          title="占支出比"
          :value="(categoryData.stats?.ratio || 0) + '%'"
          icon="fas fa-percentage"
          color="#34C759"
        />
      </div>

      <!-- 图表区域 -->
      <div class="charts-container">
        <!-- 月度趋势 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">月度趋势</h3>
          </div>
          <div ref="trendChartRef" class="chart-body"></div>
        </div>

        <!-- 时间分布 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">时间段分布</h3>
          </div>
          <div ref="timeChartRef" class="chart-body"></div>
        </div>

        <!-- 金额分布 -->
        <div class="chart-card full-width">
          <div class="chart-header">
            <h3 class="chart-title">金额分布</h3>
          </div>
          <div ref="distributionChartRef" class="chart-body"></div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <i class="fas fa-tags empty-icon"></i>
      <p>请选择分类查看分析</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import StatCard from '@/components/common/StatCard.vue'
import { formatMoney, getCategoryColor } from '@/utils/format'
import * as echarts from 'echarts'

const dataStore = useDataStore()
const uiStore = useUiStore()

const filters = ref({
  year: null,
  category: null
})

const categoryData = ref(null)

// 图表引用
const trendChartRef = ref(null)
const timeChartRef = ref(null)
const distributionChartRef = ref(null)

// 图表实例
let trendChart = null
let timeChart = null
let distributionChart = null

async function loadData() {
  if (!filters.value.year || !filters.value.category) {
    categoryData.value = null
    return
  }

  try {
    uiStore.setGlobalLoading(true)
    categoryData.value = await dataStore.loadCategoryData({
      year: filters.value.year,
      category: filters.value.category
    })

    await nextTick()
    initCharts()
  } catch (error) {
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function getCategoryIcon(category) {
  const icons = {
    '餐饮美食': 'fas fa-utensils',
    '交通出行': 'fas fa-car',
    '服饰装扮': 'fas fa-tshirt',
    '日用百货': 'fas fa-shopping-basket',
    '数码电器': 'fas fa-mobile-alt',
    '生活服务': 'fas fa-concierge-bell',
    '医疗健康': 'fas fa-heartbeat',
    '教育培训': 'fas fa-graduation-cap',
    '文化休闲': 'fas fa-gamepad',
    '住房物业': 'fas fa-home',
    '酒店旅游': 'fas fa-plane'
  }
  return icons[category] || 'fas fa-tag'
}

function initCharts() {
  initTrendChart()
  initTimeChart()
  initDistributionChart()
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  trendChart?.resize()
  timeChart?.resize()
  distributionChart?.resize()
}

function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart = echarts.init(trendChartRef.value)

  const trendData = categoryData.value?.trend || { dates: [], amounts: [] }

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>¥${param.value.toLocaleString()}`
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
      data: trendData.dates
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '金额',
      type: 'line',
      smooth: true,
      data: trendData.amounts,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: getCategoryColor(filters.value.category) + '4D' },
          { offset: 1, color: getCategoryColor(filters.value.category) + '0D' }
        ])
      },
      lineStyle: {
        color: getCategoryColor(filters.value.category),
        width: 2
      },
      itemStyle: {
        color: getCategoryColor(filters.value.category)
      }
    }]
  }

  trendChart.setOption(option)
}

function initTimeChart() {
  if (!timeChartRef.value) return

  timeChart = echarts.init(timeChartRef.value)

  const patternData = categoryData.value?.pattern || { hours: [], counts: [] }

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}:00<br/>${param.value} 笔`
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
      type: 'category',
      data: patternData.hours
    },
    yAxis: {
      type: 'value',
      name: '笔数'
    },
    series: [{
      type: 'bar',
      data: patternData.counts,
      itemStyle: {
        color: (params) => {
          const hour = params.dataIndex
          const isNight = hour >= 22 || hour <= 6
          return isNight ? '#5856D6' : '#007AFF'
        },
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }

  timeChart.setOption(option)
}

function initDistributionChart() {
  if (!distributionChartRef.value) return

  distributionChart = echarts.init(distributionChartRef.value)

  const distributionData = categoryData.value?.distribution || { ranges: [], counts: [] }

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}</>${param.value} 笔`
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
      type: 'category',
      data: distributionData.ranges
    },
    yAxis: {
      type: 'value',
      name: '笔数'
    },
    series: [{
      type: 'bar',
      data: distributionData.counts,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#FF9500' },
          { offset: 1, color: '#FF6B22' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }

  distributionChart.setOption(option)
}

onMounted(async () => {
  await dataStore.loadAvailableYears()
  await dataStore.loadCategories()
  // 默认选择当前年份和第一个分类
  const currentYear = new Date().getFullYear()
  if (dataStore.availableYears.includes(currentYear)) {
    filters.value.year = currentYear
  }
  if (dataStore.categories.length > 0) {
    filters.value.category = dataStore.categories[0]
    await loadData()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  timeChart?.dispose()
  distributionChart?.dispose()
})
</script>

<style scoped>
.category-page {
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
