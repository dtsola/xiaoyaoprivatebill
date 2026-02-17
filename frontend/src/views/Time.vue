<template>
  <div class="time-page">
    <div class="page-header">
      <h1 class="page-title">时间分析</h1>
      <div class="control-group">
        <button @click="prevYear" class="control-button" :disabled="!canGoPrev">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="control-display">{{ currentYear }}年</span>
        <button @click="nextYear" class="control-button" :disabled="!canGoNext">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !timeData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="timeData" class="time-content">
      <!-- 每日消费热力图 -->
      <div class="analysis-card">
        <div class="chart-header">
          <h2 class="card-title">每日消费热力图</h2>
          <div class="chart-controls">
            <button
              class="chart-control-btn"
              :class="{ active: currentDataType === 'expense' }"
              @click="setDataType('expense')"
            >
              支出金额
            </button>
            <button
              class="chart-control-btn"
              :class="{ active: currentDataType === 'income' }"
              @click="setDataType('income')"
            >
              收入金额
            </button>
            <button
              class="chart-control-btn"
              :class="{ active: currentDataType === 'transaction' }"
              @click="setDataType('transaction')"
            >
              交易笔数
            </button>
          </div>
        </div>
        <div class="chart-container" ref="calendarHeatmapRef"></div>
      </div>

      <!-- 日内时段分布 -->
      <div class="analysis-card">
        <div class="card-header">
          <h2 class="card-title">日内时段分布</h2>
        </div>
        <div class="chart-container" ref="hourlyChartRef"></div>
      </div>

      <!-- 工作日/周末分布 -->
      <div class="analysis-card">
        <div class="card-header">
          <h2 class="card-title">工作日/周末分布</h2>
        </div>
        <div class="chart-container" ref="weekdayChartRef"></div>
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
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import { useSessionStore } from '@/stores/session'
import { useFilterStore } from '@/stores/filter'
import { formatMoney } from '@/utils/format'
import * as echarts from 'echarts'
import api from '@/api/client'

const dataStore = useDataStore()
const uiStore = useUiStore()
const sessionStore = useSessionStore()
const filterStore = useFilterStore()

// 状态
const currentYear = ref(new Date().getFullYear())
const availableYears = ref([])
const currentDataType = ref('expense') // expense, income, transaction
const timeData = ref(null)
const heatmapData = ref({
  expense: [],
  income: [],
  transaction: [],
  expense_quantiles: [],
  income_quantiles: []
})

// 图表引用
const calendarHeatmapRef = ref(null)
const hourlyChartRef = ref(null)
const weekdayChartRef = ref(null)

// 图表实例
let heatmapChart = null
let hourlyChart = null
let weekdayChart = null

// 计算属性
const canGoPrev = computed(() => {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  return currentIndex < availableYears.value.length - 1
})

const canGoNext = computed(() => {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  return currentIndex > 0
})

// 方法
function prevYear() {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  if (currentIndex < availableYears.value.length - 1) {
    currentYear.value = availableYears.value[currentIndex + 1]
    loadData(currentYear.value)
  }
}

function nextYear() {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  if (currentIndex > 0) {
    currentYear.value = availableYears.value[currentIndex - 1]
    loadData(currentYear.value)
  }
}

function setDataType(type) {
  currentDataType.value = type
  updateHeatmap()
}

async function loadData(year) {
  try {
    console.log('[Time] Loading data for year:', year, 'filter:', filterStore.currentFilter)
    uiStore.setGlobalLoading(true)

    // 加载热力图数据
    const dailyParams = {
      year: year,
      ...filterStore.getFilterParams()
    }
    const dailyDataResponse = await api.getDailyData(dailyParams)
    console.log('[Time] Daily data response:', dailyDataResponse)

    heatmapData.value = {
      expense: dailyDataResponse.expense || [],
      income: dailyDataResponse.income || [],
      transaction: dailyDataResponse.transaction || [],
      expense_quantiles: dailyDataResponse.expense_quantiles || [],
      income_quantiles: dailyDataResponse.income_quantiles || []
    }

    // 加载时间分析数据
    const timeParams = {
      year: year,
      ...filterStore.getFilterParams()
    }
    const timeAnalysisResponse = await api.getTimeAnalysis(timeParams)
    console.log('[Time] Time analysis response:', timeAnalysisResponse)

    timeData.value = timeAnalysisResponse

    await nextTick()
    initCharts()
    updateHeatmap()
  } catch (error) {
    console.error('[Time] Failed to load data:', error)
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function initCharts() {
  if (!calendarHeatmapRef.value || !hourlyChartRef.value || !weekdayChartRef.value) return

  if (!heatmapChart) {
    heatmapChart = echarts.init(calendarHeatmapRef.value)
  }
  if (!hourlyChart) {
    hourlyChart = echarts.init(hourlyChartRef.value)
  }
  if (!weekdayChart) {
    weekdayChart = echarts.init(weekdayChartRef.value)
  }

  updateHourlyChart()
  updateWeekdayChart()

  window.addEventListener('resize', handleResize)
}

function handleResize() {
  heatmapChart?.resize()
  hourlyChart?.resize()
  weekdayChart?.resize()
}

function updateHeatmap() {
  if (!heatmapChart) return

  const rawData = heatmapData.value[currentDataType.value] || []

  // 更新按钮状态
  // 按钮状态在模板中通过 :class 处理

  // 生成全年每一天的数据
  const dateMap = new Map(rawData.map(item => [item[0], item[1]]))
  const fullData = []
  const start = new Date(currentYear.value, 0, 1)
  const end = new Date(currentYear.value, 11, 31)

  for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const dateStr = `${year}-${month}-${day}`
    const val = dateMap.get(dateStr) || dateMap.get(dateStr.replace(/-/g, '/')) || 0
    fullData.push([dateStr, val])
  }

  // 动态计算单元格大小以保持正方形
  const containerWidth = calendarHeatmapRef.value.clientWidth
  const cellSide = Math.floor((containerWidth - 60) / 54)
  const cellSize = [cellSide, cellSide]

  // 动态设置高度
  const chartHeight = 140 + 7 * cellSide + 40
  calendarHeatmapRef.value.style.height = chartHeight + 'px'
  heatmapChart.resize()

  // 确定最大值
  let maxValue
  if (currentDataType.value === 'transaction') {
    maxValue = Math.max(...rawData.map(item => item[1]), 1)
  } else if (currentDataType.value === 'expense') {
    maxValue = Math.max(...heatmapData.value.expense_quantiles, 1)
  } else {
    maxValue = Math.max(...heatmapData.value.income_quantiles, 1)
  }

  const option = {
    title: {
      top: 25,
      left: 'center',
      text: currentDataType.value === 'expense' ? '日支出金额分布' :
            currentDataType.value === 'income' ? '日收入金额分布' : '日交易笔数分布'
    },
    tooltip: {
      position: 'top',
      formatter: (params) => {
        const value = params.data[1]
        if (currentDataType.value === 'transaction') {
          return `${params.data[0]}<br>${value} 笔交易`
        } else {
          return `${params.data[0]}<br>${formatMoney(value)} 元`
        }
      }
    },
    visualMap: {
      min: 0,
      max: maxValue,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      top: 65,
      precision: 0,
      textStyle: {
        color: '#333'
      },
      inRange: {
        // GitHub 风格的绿色渐变
        color: ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
      }
    },
    calendar: {
      top: 140,
      left: 30,
      right: 30,
      cellSize: cellSize,
      range: [`${currentYear.value}/01/01`, `${currentYear.value}/12/31`],
      itemStyle: {
        color: 'transparent',
        borderWidth: 0,
        borderColor: 'transparent'
      },
      yearLabel: { show: false },
      dayLabel: {
        firstDay: 1,
        nameMap: ['日', '一', '二', '三', '四', '五', '六'],
        color: '#999'
      },
      monthLabel: {
        nameMap: 'cn',
        color: '#999'
      },
      splitLine: {
        show: false
      }
    },
    series: {
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: fullData,
      itemStyle: {
        borderRadius: 4,
        borderColor: '#fff',
        borderWidth: 3
      },
      label: {
        show: false
      }
    }
  }

  heatmapChart.setOption(option, true)
}

function updateHourlyChart() {
  if (!hourlyChart || !timeData.value) return

  const hourly = timeData.value.hourly || {
    amounts: Array(24).fill(0),
    counts: Array(24).fill(0)
  }

  const option = {
    title: {
      text: '日内消费时段分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(param => {
          if (param.seriesName === '消费金额') {
            result += param.marker + param.seriesName + ': ' + formatMoney(param.value) + ' 元<br/>'
          } else {
            result += param.marker + param.seriesName + ': ' + param.value + ' 笔<br/>'
          }
        })
        return result
      }
    },
    legend: {
      data: ['消费金额', '交易笔数'],
      top: 30
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: Array.from({ length: 24 }, (_, i) => `${i}时`),
      axisLabel: {
        interval: 0
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '金额（元）'
      },
      {
        type: 'value',
        name: '笔数',
        position: 'right'
      }
    ],
    series: [
      {
        name: '消费金额',
        type: 'bar',
        data: hourly.amounts,
        itemStyle: {
          color: '#1890ff',
          borderRadius: [4, 4, 0, 0]
        }
      },
      {
        name: '交易笔数',
        type: 'line',
        yAxisIndex: 1,
        data: hourly.counts,
        itemStyle: {
          color: '#FF9500'
        }
      }
    ]
  }

  hourlyChart.setOption(option, true)
}

function updateWeekdayChart() {
  if (!weekdayChart || !timeData.value) return

  const weekdayWeekend = timeData.value.weekday_weekend || {}

  // 过滤掉总金额为0的分类
  const filteredCategories = Object.entries(weekdayWeekend)
    .filter(([_, values]) => (values?.weekday?.amount || 0) > 0 || (values?.weekend?.amount || 0) > 0)
    .reduce((acc, [key, value]) => {
      acc[key] = value
      return acc
    }, {})

  const categories = Object.keys(filteredCategories)

  const weekdayData = categories.map(cat => {
    const percentage = filteredCategories[cat]?.weekday?.percentage || 0
    const item = { value: percentage }
    if (percentage >= 99.9) {
      item.itemStyle = { borderRadius: 4 }
    }
    return item
  })

  const weekendData = categories.map(cat => {
    const percentage = filteredCategories[cat]?.weekend?.percentage || 0
    const item = { value: percentage }
    if (percentage >= 99.9) {
      item.itemStyle = { borderRadius: 4 }
    }
    return item
  })

  // 动态调整图表高度
  const categoryCount = categories.length
  const autoHeight = Math.max(categoryCount * 35 + 80, 250)
  weekdayChartRef.value.style.height = autoHeight + 'px'
  weekdayChart.resize()

  const option = {
    title: {
      text: '工作日/周末消费分布',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: '600',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(param => {
          result += param.marker + param.seriesName + ': ' + param.value.toFixed(2) + '%<br/>'
        })
        return result
      }
    },
    legend: {
      data: ['工作日', '周末'],
      top: 40,
      itemWidth: 12,
      itemHeight: 12,
      icon: 'circle',
      textStyle: {
        fontSize: 13,
        color: '#666'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '80',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: 100,
      splitLine: {
        show: false
      },
      axisLabel: {
        show: false
      }
    },
    yAxis: {
      type: 'category',
      data: categories,
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        fontSize: 14,
        color: '#333',
        fontWeight: '500',
        margin: 16
      }
    },
    series: [
      {
        name: '工作日',
        type: 'bar',
        stack: 'total',
        barWidth: 24,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#007AFF' },
            { offset: 1, color: '#5AC8FA' }
          ]),
          borderRadius: [4, 0, 0, 4]
        },
        label: {
          show: true,
          position: 'inside',
          formatter: (params) => params.value > 10 ? params.value.toFixed(0) + '%' : '',
          color: '#fff',
          fontWeight: 'bold'
        },
        data: weekdayData
      },
      {
        name: '周末',
        type: 'bar',
        stack: 'total',
        barWidth: 24,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#FF9500' },
            { offset: 1, color: '#FFB340' }
          ]),
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'inside',
          formatter: (params) => params.value > 10 ? params.value.toFixed(0) + '%' : '',
          color: '#fff',
          fontWeight: 'bold'
        },
        data: weekendData
      }
    ]
  }

  weekdayChart.setOption(option, true)
}

// 监听筛选器变化
watch(() => filterStore.currentFilter, () => {
  if (currentYear.value) {
    loadData(currentYear.value)
  }
})

onMounted(async () => {
  try {
    uiStore.setGlobalLoading(true)

    // 加载可用年份
    await dataStore.loadAvailableYears()
    availableYears.value = dataStore.availableYears.sort((a, b) => b - a)

    if (availableYears.value.length > 0) {
      currentYear.value = availableYears.value[0]

      // 如果进入演示模式，稍作延迟以确保数据已准备好
      if (sessionStore.isDemo) {
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      await loadData(currentYear.value)
    }
  } catch (error) {
    console.error('Time page init error:', error)
    uiStore.showError('页面初始化失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  heatmapChart?.dispose()
  hourlyChart?.dispose()
  weekdayChart?.dispose()
})
</script>

<style scoped>
.time-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 20px;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-button {
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

.control-button:hover:not(:disabled) {
  background: var(--hover-bg);
  border-color: var(--primary-color);
}

.control-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.control-display {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  min-width: 80px;
  text-align: center;
}

.analysis-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
  height: auto;
  min-height: 400px;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.chart-controls {
  display: flex;
  gap: 12px;
}

.chart-control-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: var(--card-bg);
  color: var(--secondary-text);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chart-control-btn:hover {
  background: var(--hover-bg);
}

.chart-control-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.card-header {
  margin-bottom: 16px;
}

.chart-container {
  height: 400px;
}

#calendarHeatmap {
  min-height: 280px;
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

@media (max-width: 768px) {
  .page-header {
    grid-template-columns: 1fr;
    gap: 16px;
    text-align: center;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
