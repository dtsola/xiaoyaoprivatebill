<template>
  <div class="time-page">
    <div class="page-header">
      <h1 class="page-title">时间分析</h1>
      <div class="header-actions">
        <select v-model="filters.year" @change="loadData" class="filter-select">
          <option value="">选择年份</option>
          <option v-for="year in dataStore.availableYears" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !timeData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="timeData" class="time-content">
      <!-- 图表区域 -->
      <div class="charts-container">
        <!-- 每日热力图 -->
        <div class="chart-card full-width">
          <div class="chart-header">
            <h3 class="chart-title">每日消费热力图</h3>
          </div>
          <div ref="heatmapChartRef" class="chart-body heatmap-body"></div>
        </div>

        <!-- 工作日 vs 周末 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">工作日 vs 周末</h3>
          </div>
          <div ref="weekendChartRef" class="chart-body"></div>
        </div>

        <!-- 时段分布 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">消费时段分布</h3>
          </div>
          <div ref="hourlyChartRef" class="chart-body"></div>
        </div>

        <!-- 周消费模式 -->
        <div class="chart-card full-width">
          <div class="chart-header">
            <h3 class="chart-title">每周消费模式</h3>
          </div>
          <div ref="weeklyChartRef" class="chart-body"></div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <i class="fas fa-clock empty-icon"></i>
      <p>请选择年份查看时间分析</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import { formatMoney } from '@/utils/format'
import * as echarts from 'echarts'

const dataStore = useDataStore()
const uiStore = useUiStore()

const filters = ref({
  year: null
})

const timeData = ref(null)

// 图表引用
const heatmapChartRef = ref(null)
const weekendChartRef = ref(null)
const hourlyChartRef = ref(null)
const weeklyChartRef = ref(null)

// 图表实例
let heatmapChart = null
let weekendChart = null
let hourlyChart = null
let weeklyChart = null

async function loadData() {
  if (!filters.value.year) {
    timeData.value = null
    return
  }

  try {
    uiStore.setGlobalLoading(true)
    timeData.value = await dataStore.loadTimeData({
      year: filters.value.year
    })

    await nextTick()
    initCharts()
  } catch (error) {
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function initCharts() {
  initHeatmapChart()
  initWeekendChart()
  initHourlyChart()
  initWeeklyChart()
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  heatmapChart?.resize()
  weekendChart?.resize()
  hourlyChart?.resize()
  weeklyChart?.resize()
}

function initHeatmapChart() {
  if (!heatmapChartRef.value) return

  heatmapChart = echarts.init(heatmapChartRef.value)

  const dailyData = timeData.value?.daily_data || {}
  const dates = Object.keys(dailyData).sort()

  // 生成热力图数据
  const heatmapData = []
  const yearData = {}

  dates.forEach(date => {
    const [year, month, day] = date.split('-')
    const monthIndex = parseInt(month) - 1
    const dayIndex = parseInt(day) - 1

    if (!yearData[monthIndex]) {
      yearData[monthIndex] = {}
    }
    yearData[monthIndex][dayIndex] = dailyData[date]

    heatmapData.push([
      parseInt(month),
      parseInt(day),
      dailyData[date]
    ])
  })

  const option = {
    tooltip: {
      position: 'top',
      formatter: (params) => {
        const [month, day, value] = params.value
        return `${month}月${day}日<br/>¥${value ? value.toLocaleString() : 0}`
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...heatmapData.map(d => d[2])),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#E8F5E9', '#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20']
      }
    },
    calendar: {
      top: '15%',
      left: '10%',
      right: '5%',
      cellSize: ['auto', 16],
      range: filters.value.year ? new Date(filters.value.year, 0, 1) : new Date(),
      yearLabel: { show: false },
      monthLabel: {
        nameMap: 'cn',
        fontSize: 12
      },
      dayLabel: {
        nameMap: 'cn',
        fontSize: 11,
        firstDay: 1
      },
      itemStyle: {
        borderWidth: 2,
        borderColor: '#fff'
      }
    },
    series: [{
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: heatmapData
    }]
  }

  heatmapChart.setOption(option)
}

function initWeekendChart() {
  if (!weekendChartRef.value) return

  weekendChart = echarts.init(weekendChartRef.value)

  const comparison = timeData.value?.weekend_comparison || {
    weekday: 0,
    weekend: 0
  }

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        return `${params.name}<br/>¥${params.value.toLocaleString()}`
      }
    },
    series: [{
      name: '消费金额',
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: comparison.weekday, name: '工作日' },
        { value: comparison.weekend, name: '周末' }
      ],
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: (params) => {
          return `${params.name}\n¥${params.value.toLocaleString()}`
        }
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      }
    }]
  }

  weekendChart.setOption(option)
}

function initHourlyChart() {
  if (!hourlyChartRef.value) return

  hourlyChart = echarts.init(hourlyChartRef.value)

  const hourlyData = timeData.value?.hourly_analysis || { hours: [], amounts: [] }

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}:00<br/>¥${param.value.toLocaleString()}`
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
      data: hourlyData.hours || Array.from({ length: 24 }, (_, i) => i)
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      type: 'bar',
      data: hourlyData.amounts || [],
      itemStyle: {
        color: (params) => {
          const hour = params.dataIndex
          // 凌晨时段用紫色，白天用蓝色，晚上用橙色
          if (hour >= 0 && hour < 6) return '#AF52DE'
          if (hour >= 6 && hour < 12) return '#007AFF'
          if (hour >= 12 && hour < 18) return '#34C759'
          return '#FF9500'
        },
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }

  hourlyChart.setOption(option)
}

function initWeeklyChart() {
  if (!weeklyChartRef.value) return

  weeklyChart = echarts.init(weeklyChartRef.value)

  const weeklyData = timeData.value?.weekly_pattern || {
    weekdays: [],
    amounts: []
  }

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
      data: weeklyData.weekdays || ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '消费金额',
      type: 'line',
      smooth: true,
      data: weeklyData.amounts || [],
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0, 122, 255, 0.3)' },
            { offset: 1, color: 'rgba(0, 122, 255, 0.05)' }
          ])
        },
        lineStyle: {
          color: '#007AFF',
          width: 2
        },
        itemStyle: {
          color: '#007AFF'
        }
      }]
  }

  weeklyChart.setOption(option)
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
  heatmapChart?.dispose()
  weekendChart?.dispose()
  hourlyChart?.dispose()
  weeklyChart?.dispose()
})
</script>

<style scoped>
.time-page {
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

.heatmap-body {
  height: 280px;
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>
