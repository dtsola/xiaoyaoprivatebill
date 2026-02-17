<template>
  <div class="category-page">
    <!-- 页面头部 -->
    <div class="category-page-header">
      <div class="header-left">
        <h1 class="page-title">分类分析</h1>
        <div class="category-selector">
          <div class="selected-category" @click="toggleCategoryExpanded">
            <div class="category-pill active">
              <span class="icon" :style="{ backgroundColor: getCategoryColor(currentCategory) }"></span>
              <span>{{ currentCategory }}</span>
              <i class="fas fa-chevron-down dropdown-icon"></i>
            </div>
          </div>
          <div class="category-expanded" v-show="categoryExpanded" @click.stop>
            <div class="category-pills">
              <!-- 支付宝分类 -->
              <template v-if="categoryGroups.alipay && categoryGroups.alipay.length > 0">
                <div class="category-divider">
                  <span><i class="fab fa-alipay" style="color: #1677FF;"></i> 支付宝</span>
                  <div class="line"></div>
                </div>
                <div
                  v-for="cat in categoryGroups.alipay"
                  :key="cat"
                  class="category-pill"
                  :class="{ active: cat === currentCategory }"
                  @click.stop="selectCategory(cat)"
                >
                  <span class="icon" :style="{ backgroundColor: getCategoryColor(cat) }"></span>
                  <span>{{ cat }}</span>
                </div>
              </template>

              <!-- 微信分类 -->
              <template v-if="categoryGroups.wechat && categoryGroups.wechat.length > 0">
                <div class="category-divider">
                  <span><i class="fab fa-weixin" style="color: #07C160;"></i> 微信</span>
                  <div class="line"></div>
                </div>
                <div
                  v-for="cat in categoryGroups.wechat"
                  :key="cat"
                  class="category-pill"
                  :class="{ active: cat === currentCategory }"
                  @click.stop="selectCategory(cat)"
                >
                  <span class="icon" :style="{ backgroundColor: getCategoryColor(cat) }"></span>
                  <span>{{ cat }}</span>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <div class="time-range-selector">
        <button class="time-button" @click="prevTime" :disabled="!canGoPrev" v-show="timeRange !== 'all'">
          <i class="fas fa-chevron-left"></i>
        </button>
        <div class="time-display">
          <span>{{ timeDisplay }}</span>
        </div>
        <button class="time-button" @click="nextTime" :disabled="!canGoNext" v-show="timeRange !== 'all'">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>

      <div class="category-range-selector">
        <button class="range-btn" :class="{ active: timeRange === 'all' }" @click="setTimeRange('all')">所有</button>
        <button class="range-btn" :class="{ active: timeRange === 'year' }" @click="setTimeRange('year')">年度</button>
        <button class="range-btn" :class="{ active: timeRange === 'month' }" @click="setTimeRange('month')">月度</button>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !categoryData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="categoryData" class="category-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>分类总支出</h3>
          <div class="value">{{ formatMoney(categoryData.stats?.total_expense || 0) }} 元</div>
          <div class="trend">
            <span>{{ categoryData.stats?.transaction_count || 0 }} 笔交易</span>
            <span style="margin-left: 8px">平均 {{ formatMoney(categoryData.stats?.avg_amount || 0) }} 元/笔</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>支出占比</h3>
          <div class="value">{{ (categoryData.stats?.expense_ratio || 0).toFixed(1) }}%</div>
          <div class="trend">
            <span>{{ categoryData.stats?.total_expense > 0 ? '占总支出比例' : '暂无数据' }}</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>月均支出</h3>
          <div class="value">{{ monthlyAvgValue }} 元</div>
          <div class="trend">
            <span>{{ monthlyAvgLabel }}</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>消费频率</h3>
          <div class="value">{{ frequencyValue }} 次</div>
          <div class="trend">
            <span>{{ frequencyLabel }}</span>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="chart">
        <div class="chart-header">
          <h2 class="chart-title">支出趋势</h2>
        </div>
        <div class="chart-container" ref="trendChartRef"></div>
      </div>

      <div class="chart">
        <div class="chart-header">
          <h2 class="chart-title">消费规律分析</h2>
        </div>
        <div class="chart-container" ref="patternChartRef"></div>
      </div>

      <div class="chart">
        <div class="chart-header">
          <h2 class="chart-title">金额分布</h2>
        </div>
        <div class="chart-container" ref="distributionChartRef"></div>
      </div>
    </div>

    <div v-else class="empty-state">
      <i class="fas fa-chart-bar empty-icon"></i>
      <p>暂无数据</p>
      <button class="btn btn-primary" @click="$router.push('/settings')">
        上传账单
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useSessionStore } from '@/stores/session'
import { useFilterStore } from '@/stores/filter'
import { formatMoney, getCategoryColor } from '@/utils/format'
import * as echarts from 'echarts'
import api from '@/api/client'

const uiStore = useUiStore()
const sessionStore = useSessionStore()
const filterStore = useFilterStore()

// 状态
const currentCategory = ref(null)
const timeRange = ref('year') // all, year, month
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const availableYears = ref([])
const availableMonths = ref({})
const categoryExpanded = ref(false)
const categoryData = ref(null)
const categoryGroups = ref({ alipay: [], wechat: [] })
const allCategories = ref([])

// 图表引用
const trendChartRef = ref(null)
const patternChartRef = ref(null)
const distributionChartRef = ref(null)

// 图表实例
let trendChart = null
let patternChart = null
let distributionChart = null

// 计算属性
const timeDisplay = computed(() => {
  if (timeRange.value === 'all') return '全部时间'
  if (timeRange.value === 'year') return `${currentYear.value}年`
  return `${currentYear.value}年${currentMonth.value}月`
})

const canGoPrev = computed(() => {
  if (timeRange.value === 'all') return false
  if (timeRange.value === 'year') {
    return currentYear.value > Math.min(...availableYears.value)
  }
  // month
  const currentYearMonths = availableMonths.value[currentYear.value] || []
  const minMonth = Math.min(...currentYearMonths)
  const isFirstMonth = currentMonth.value <= minMonth && currentYear.value <= Math.min(...availableYears.value)
  return !isFirstMonth
})

const canGoNext = computed(() => {
  if (timeRange.value === 'all') return false
  if (timeRange.value === 'year') {
    return currentYear.value < Math.max(...availableYears.value)
  }
  // month
  const currentYearMonths = availableMonths.value[currentYear.value] || []
  const maxMonth = Math.max(...currentYearMonths)
  const isLastMonth = currentMonth.value >= maxMonth && currentYear.value >= Math.max(...availableYears.value)
  return !isLastMonth
})

const monthlyAvgValue = computed(() => {
  const stats = categoryData.value?.stats
  if (!stats) return '0'

  if (timeRange.value === 'all') {
    // 所有时间范围
    const monthlyAvg = stats.total_expense / (stats.date_range / 30)
    return formatMoney(monthlyAvg)
  } else if (timeRange.value === 'year') {
    // 年度范围
    const monthlyAvg = stats.total_expense / 12
    return formatMoney(monthlyAvg)
  } else {
    // 月度范围
    return formatMoney(stats.total_expense)
  }
})

const monthlyAvgLabel = computed(() => {
  if (timeRange.value === 'all') return '历史月均支出'
  if (timeRange.value === 'year') return '月均支出'
  return '本月支出'
})

const frequencyValue = computed(() => {
  const stats = categoryData.value?.stats
  if (!stats) return '0.0'

  if (timeRange.value === 'all') {
    const frequency = stats.transaction_count / stats.date_range
    return frequency.toFixed(1)
  } else if (timeRange.value === 'year') {
    const frequency = stats.transaction_count / 365
    return frequency.toFixed(1)
  } else {
    const daysInMonth = new Date(currentYear.value, currentMonth.value, 0).getDate()
    const frequency = stats.transaction_count / daysInMonth
    return frequency.toFixed(1)
  }
})

const frequencyLabel = computed(() => {
  if (timeRange.value === 'all') return '历史日均交易'
  return '日均交易频率'
})

// 方法
function toggleCategoryExpanded() {
  categoryExpanded.value = !categoryExpanded.value
}

function selectCategory(category) {
  currentCategory.value = category
  categoryExpanded.value = false
  loadCategoryData(category)
}

function setTimeRange(range) {
  timeRange.value = range
  if (currentCategory.value) {
    loadCategoryData(currentCategory.value)
  }
}

function prevTime() {
  if (timeRange.value === 'year') {
    if (currentYear.value > Math.min(...availableYears.value)) {
      currentYear.value--
      if (availableMonths.value[currentYear.value]) {
        currentMonth.value = Math.max(...availableMonths.value[currentYear.value])
      }
    }
  } else if (timeRange.value === 'month') {
    if (currentMonth.value > 1) {
      currentMonth.value--
    } else if (currentYear.value > Math.min(...availableYears.value)) {
      currentYear.value--
      currentMonth.value = 12
    }
    // 确保月份在可用范围内
    if (availableMonths.value[currentYear.value]) {
      const validMonths = availableMonths.value[currentYear.value]
      if (!validMonths.includes(currentMonth.value)) {
        currentMonth.value = Math.max(...validMonths.filter(m => m < currentMonth.value))
      }
    }
  }

  if (currentCategory.value) {
    loadCategoryData(currentCategory.value)
  }
}

function nextTime() {
  if (timeRange.value === 'year') {
    if (currentYear.value < Math.max(...availableYears.value)) {
      currentYear.value++
      if (availableMonths.value[currentYear.value]) {
        currentMonth.value = Math.min(...availableMonths.value[currentYear.value])
      }
    }
  } else if (timeRange.value === 'month') {
    if (currentMonth.value < 12) {
      currentMonth.value++
    } else if (currentYear.value < Math.max(...availableYears.value)) {
      currentYear.value++
      currentMonth.value = 1
    }
    // 确保月份在可用范围内
    if (availableMonths.value[currentYear.value]) {
      const validMonths = availableMonths.value[currentYear.value]
      if (!validMonths.includes(currentMonth.value)) {
        currentMonth.value = Math.min(...validMonths.filter(m => m > currentMonth.value))
      }
    }
  }

  if (currentCategory.value) {
    loadCategoryData(currentCategory.value)
  }
}

async function loadCategories() {
  try {
    console.log('[Category] Loading categories...')
    const data = await api.getCategoryAnalysis()
    console.log('[Category] Category analysis response:', data)

    if (!data.categories || data.categories.length === 0) {
      uiStore.showError('暂无分类数据')
      return
    }

    allCategories.value = data.categories || []

    // 分组分类
    if (data.category_groups) {
      categoryGroups.value = data.category_groups
    } else {
      // 兼容：如果没有分组，将所有分类放入支付宝组
      categoryGroups.value = {
        alipay: data.categories || [],
        wechat: []
      }
    }

    // 默认选中第一个分类
    const defaultCategory = data.categories[0]
    currentCategory.value = defaultCategory

    await loadCategoryData(defaultCategory)
  } catch (error) {
    console.error('[Category] Failed to load categories:', error)
    uiStore.showError('加载分类失败: ' + error.message)
  }
}

async function loadAvailableDates() {
  try {
    console.log('[Category] Loading available dates...')
    const data = await api.getCategoryAvailableDates()
    console.log('[Category] Available dates response:', data)

    availableYears.value = data.years || []
    availableMonths.value = data.months || {}

    // 设置默认年份为最新的年份
    if (availableYears.value.length > 0) {
      currentYear.value = Math.max(...availableYears.value)
      // 设置默认月份为当年的最新月份
      if (availableMonths.value[currentYear.value]) {
        currentMonth.value = Math.max(...availableMonths.value[currentYear.value])
      }
    }
  } catch (error) {
    console.error('[Category] Failed to load available dates:', error)
  }
}

async function loadCategoryData(category) {
  if (!category) return

  try {
    console.log('[Category] Loading category data:', category, 'timeRange:', timeRange.value)

    const params = {
      category: category,
      range: timeRange.value,
      year: currentYear.value.toString(),
      month: currentMonth.value.toString(),
      ...filterStore.getFilterParams()
    }

    const data = await api.getCategoryAnalysis(params)
    console.log('[Category] Category data loaded:', data)

    categoryData.value = data

    await nextTick()
    initCharts()
  } catch (error) {
    console.error('[Category] Failed to load category data:', error)
    uiStore.showError('加载数据失败: ' + error.message)
  }
}

function initCharts() {
  if (!trendChartRef.value || !patternChartRef.value || !distributionChartRef.value) return

  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
  }
  if (!patternChart) {
    patternChart = echarts.init(patternChartRef.value)
  }
  if (!distributionChart) {
    distributionChart = echarts.init(distributionChartRef.value)
  }

  updateCharts()

  window.addEventListener('resize', handleResize)
}

function handleResize() {
  trendChart?.resize()
  patternChart?.resize()
  distributionChart?.resize()
}

function updateCharts() {
  if (!categoryData.value) return

  initTrendChart()
  initPatternChart()
  initDistributionChart()
}

function initTrendChart() {
  if (!trendChart || !categoryData.value) return

  const trend = categoryData.value.trend || { dates: [], amounts: [], counts: [], ratios: [] }
  const hasData = trend.dates && trend.dates.length > 0

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        if (!hasData) return '暂无数据'
        const date = params[0].name
        const amount = params[0].value
        const ratio = params[1] ? params[1].value : 0
        const count = trend.counts[params[0].dataIndex] || 0

        let dateLabel
        if (timeRange.value === 'all') {
          dateLabel = `${date}年`
        } else if (timeRange.value === 'year') {
          const parts = date.split('-')
          dateLabel = `${parts[0]}年${parts[1]}月`
        } else {
          dateLabel = date
        }

        if (amount === 0) {
          return `${dateLabel}<br/>无交易记录`
        }

        return `${dateLabel}<br/>支出：${formatMoney(amount)} 元<br/>占比：${ratio.toFixed(1)}%<br/>笔数：${count} 笔`
      }
    },
    legend: {
      data: ['支出金额', '支出占比'],
      top: 10,
      right: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hasData ? trend.dates : [],
      axisLabel: {
        formatter: (value) => {
          if (timeRange.value === 'all') {
            return value + '年'
          } else if (timeRange.value === 'year') {
            const parts = value.split('-')
            return parts[1] + '月'
          } else {
            const parts = value.split('-')
            return parts[2] + '日'
          }
        }
      }
    },
    yAxis: [{
      type: 'value',
      name: '金额 (元)',
      position: 'left',
      axisLabel: {
        formatter: (value) => formatMoney(value)
      }
    }, {
      type: 'value',
      name: '占比 (%)',
      position: 'right',
      splitLine: { show: false },
      axisLabel: {
        formatter: '{value}%'
      }
    }],
    series: [{
      name: '支出金额',
      type: 'bar',
      data: hasData ? trend.amounts : [],
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: getCategoryColor(currentCategory.value) + 'CC'
        }, {
          offset: 1,
          color: getCategoryColor(currentCategory.value) + '99'
        }]),
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '60%',
      z: 1
    }, {
      name: '支出占比',
      type: 'line',
      yAxisIndex: 1,
      data: hasData ? trend.ratios : [],
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: '#FF9500'
      },
      itemStyle: {
        color: '#FF9500',
        borderWidth: 2,
        borderColor: '#ffffff'
      },
      z: 2,
      smooth: 0.2
    }]
  }

  trendChart.setOption(option, true)
}

function initPatternChart() {
  if (!patternChart || !categoryData.value) return

  const pattern = categoryData.value.pattern || {
    hours: Array.from({ length: 24 }, (_, i) => i),
    counts: Array(24).fill(0),
    amounts: Array(24).fill(0)
  }

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(param => {
          if (param.seriesName === '交易金额') {
            result += param.marker + param.seriesName + ': ' + formatMoney(param.value) + ' 元<br/>'
          } else {
            result += param.marker + param.seriesName + ': ' + param.value + ' 次<br/>'
          }
        })
        return result
      }
    },
    legend: {
      data: ['交易次数', '交易金额'],
      top: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: pattern.hours.map(h => `${h}时`),
      axisLabel: {
        interval: 0
      }
    },
    yAxis: [{
      type: 'value',
      name: '交易次数',
      position: 'left'
    }, {
      type: 'value',
      name: '交易金额',
      position: 'right',
      axisLine: { show: true },
      axisLabel: {
        formatter: (value) => formatMoney(value)
      }
    }],
    series: [{
      name: '交易金额',
      type: 'line',
      yAxisIndex: 1,
      data: pattern.amounts,
      itemStyle: {
        color: getCategoryColor(currentCategory.value)
      },
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: getCategoryColor(currentCategory.value) + '40'
        }, {
          offset: 1,
          color: getCategoryColor(currentCategory.value) + '00'
        }])
      },
      z: 1
    }, {
      name: '交易次数',
      type: 'bar',
      data: pattern.counts,
      itemStyle: {
        color: 'rgba(128, 128, 128, 0.3)',
        borderRadius: [4, 4, 0, 0]
      },
      z: 2
    }]
  }

  patternChart.setOption(option, true)
}

function initDistributionChart() {
  if (!distributionChart || !categoryData.value) return

  const distribution = categoryData.value.distribution || {
    ranges: ['0-50', '50-100', '100-200', '200-500', '500-1000', '1000+'],
    counts: Array(6).fill(0)
  }
  const hasData = distribution.counts && distribution.counts.some(c => c > 0)

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        if (!hasData) return '暂无数据'
        const range = params[0].name
        const count = params[0].value
        const total = distribution.counts.reduce((a, b) => a + b, 0)
        const percentage = ((count / total) * 100).toFixed(2)
        return `金额范围：${range}<br/>交易笔数：${count} 笔<br/>占比：${percentage}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: distribution.ranges,
      axisLabel: {
        interval: 0,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      name: '交易次数'
    },
    series: [{
      type: 'bar',
      data: distribution.counts.map((count) => ({
        value: count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
            offset: 0,
            color: getCategoryColor(currentCategory.value)
          }, {
            offset: 1,
            color: getCategoryColor(currentCategory.value) + '80'
          }]),
          borderRadius: [4, 4, 0, 0]
        }
      }))
    }]
  }

  distributionChart.setOption(option, true)
}

// 监听筛选器变化
watch(() => filterStore.currentFilter, () => {
  if (currentCategory.value) {
    loadCategoryData(currentCategory.value)
  }
})

onMounted(async () => {
  try {
    uiStore.setGlobalLoading(true)

    // 加载可用日期
    await loadAvailableDates()

    // 如果进入演示模式，稍作延迟以确保数据已准备好
    if (sessionStore.isDemo) {
      await new Promise(resolve => setTimeout(resolve, 500))
    }

    // 加载分类数据
    await loadCategories()
  } catch (error) {
    console.error('Category page init error:', error)
    uiStore.showError('页面初始化失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  patternChart?.dispose()
  distributionChart?.dispose()
})
</script>

<style scoped>
.category-page {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.category-page-header {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 20px;
  padding: 0 20px;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

/* 分类选择器 */
.category-selector {
  position: relative;
  padding: 0;
  margin: 0;
}

.category-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  color: var(--text-color);
  white-space: nowrap;
}

.category-pill .icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.category-pill.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.dropdown-icon {
  font-size: 10px;
  margin-left: 4px;
}

.category-expanded {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 0;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  padding: 12px;
  padding-top: 16px;
  z-index: 1000;
  min-width: 300px;
  max-height: 400px;
  overflow-y: auto;
}

.category-pills {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-divider {
  display: flex;
  align-items: center;
  margin: 10px 0 8px 0;
  color: #999;
  font-size: 12px;
  padding: 0 5px;
}

.category-divider span {
  margin-right: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
  font-weight: 500;
  color: #666;
}

.category-divider .line {
  flex: 1;
  height: 1px;
  background-color: #e0e0e0;
}

/* 时间范围选择器 */
.time-range-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.time-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-color);
  transition: all 0.2s ease;
}

.time-button:hover:not(:disabled) {
  background: var(--hover-bg);
  border-color: var(--primary-color);
}

.time-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.time-display {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  min-width: 100px;
  text-align: center;
}

/* 范围选择器 */
.category-range-selector {
  display: flex;
  gap: 8px;
}

.range-btn {
  padding: 8px 16px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-color);
}

.range-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.range-btn:hover:not(.active) {
  background: var(--hover-bg);
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-card);
}

.stat-card h3 {
  font-size: 14px;
  font-weight: 500;
  color: var(--secondary-text);
  margin: 0 0 12px 0;
}

.stat-card .value {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 8px;
}

.stat-card .trend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 13px;
  color: var(--secondary-text);
}

/* 图表 */
.chart {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.chart-container {
  height: 400px;
}

/* 加载和空状态 */
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

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
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

@media (max-width: 1024px) {
  .category-page-header {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
