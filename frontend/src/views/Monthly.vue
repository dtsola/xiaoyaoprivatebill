<template>
  <div class="monthly-page">
    <div class="page-header">
      <h1 class="page-title">月度分析</h1>
      <div class="control-group">
        <button @click="prevMonth" class="control-button" :disabled="!canGoPrev">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="control-display">{{ currentMonthDisplay }}</span>
        <button @click="nextMonth" class="control-button" :disabled="!canGoNext">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      <div></div>
    </div>

    <div v-if="uiStore.globalLoading && !monthlyData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="monthlyData" class="monthly-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>月度收支</h3>
          <div class="value" :style="{ color: balanceColor }">
            {{ formatMoney(Math.abs(balance)) }} 元
          </div>
          <div class="trend">
            <span>{{ balanceStatus }}</span>
            <span style="margin-left: 8px">{{ balanceRatio }}</span>
          </div>
          <div class="comparison">
            <i :class="['fas', getComparisonData('balance').icon, 'trend-icon', getComparisonData('balance').iconClass]"></i>
            <span class="change-value">{{ getComparisonData('balance').text }}</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>月度支出</h3>
          <div class="value">{{ formatMoney(monthlyData.stats?.total_expense || 0) }} 元</div>
          <div class="trend">
            <span>{{ monthlyData.stats?.expense_count || 0 }} 笔支出</span>
            <span style="margin-left: 8px">日均 {{ formatMoney(monthlyData.stats?.total_expense / 30 || 0) }} 元</span>
          </div>
          <div class="comparison">
            <i :class="['fas', getComparisonData('expense').icon, 'trend-icon', getComparisonData('expense').iconClass]"></i>
            <span class="change-value">{{ getComparisonData('expense').text }}</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>月度收入</h3>
          <div class="value">{{ formatMoney(monthlyData.stats?.total_income || 0) }} 元</div>
          <div class="trend">
            <span>{{ monthlyData.stats?.income_count || 0 }} 笔收入</span>
            <span style="margin-left: 8px">平均 {{ formatMoney(monthlyData.stats?.total_income / (monthlyData.stats?.income_count || 1) || 0) }} 元/笔</span>
          </div>
          <div class="comparison">
            <i :class="['fas', getComparisonData('income').icon, 'trend-icon', getComparisonData('income').iconClass]"></i>
            <span class="change-value">{{ getComparisonData('income').text }}</span>
          </div>
        </div>
        <div class="stat-card">
          <h3>交易情况</h3>
          <div class="value">{{ totalCount }} 笔</div>
          <div class="trend">
            <span>平均 {{ formatMoney((monthlyData.stats?.total_expense + monthlyData.stats?.total_income) / (totalCount || 1) || 0) }} 元/笔</span>
            <span style="margin-left: 8px">30 个交易日</span>
          </div>
          <div class="comparison">
            <i :class="['fas', getComparisonData('count').icon, 'trend-icon', getComparisonData('count').iconClass]"></i>
            <span class="change-value">{{ getComparisonData('count').text }}</span>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="card">
        <div class="chart-header">
          <div class="chart-title-row">
            <h2 class="chart-title">收支趋势</h2>
            <div class="chart-toggle">
              <button
                class="toggle-btn"
                :class="{ active: currentType === 'expense' }"
                @click="switchType('expense')"
              >
                <i class="fas fa-arrow-up"></i>支出
              </button>
              <button
                class="toggle-btn"
                :class="{ active: currentType === 'income' }"
                @click="switchType('income')"
              >
                <i class="fas fa-arrow-down"></i>收入
              </button>
            </div>
          </div>
        </div>
        <div class="chart-container" ref="trendChartRef"></div>
      </div>

      <div class="card">
        <div class="chart-header">
          <div class="chart-title-row">
            <h2 class="chart-title">{{ currentType === 'expense' ? '支出' : '收入' }}分类</h2>
          </div>
        </div>
        <div class="chart-container" style="display: flex; height: 500px;">
          <div ref="categoryPieChartRef" style="flex: 1; height: 100%;"></div>
          <div ref="customLegendRef" style="width: 45%; overflow-y: auto; padding: 20px;"></div>
        </div>
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
import { formatMoney, getCategoryColor } from '@/utils/format'
import * as echarts from 'echarts'

const dataStore = useDataStore()
const uiStore = useUiStore()
const sessionStore = useSessionStore()
const filterStore = useFilterStore()

const currentMonth = ref(null)
const monthlyData = ref(null)
const currentType = ref('expense')

// 图表引用
const trendChartRef = ref(null)
const categoryPieChartRef = ref(null)
const customLegendRef = ref(null)

// 图表实例
let trendChart = null
let categoryPieChart = null

// 可用月份列表
const availableMonths = ref([])

// 计算属性
const balance = computed(() => {
  const income = monthlyData.value?.stats?.total_income || 0
  const expense = monthlyData.value?.stats?.total_expense || 0
  return income - expense
})

const balanceColor = computed(() => {
  return balance.value >= 0 ? 'var(--success-color)' : 'var(--danger-color)'
})

const balanceStatus = computed(() => {
  return balance.value >= 0 ? '收大于支' : '支大于收'
})

const balanceRatio = computed(() => {
  const income = monthlyData.value?.stats?.total_income || 0
  const expense = monthlyData.value?.stats?.total_expense || 0
  if (income === 0) return '--'
  const ratio = (expense / income * 100).toFixed(2)
  if (expense > income) {
    return `超支比例 ${ratio}%`
  } else {
    return `支出占比 ${ratio}%`
  }
})

const totalCount = computed(() => {
  return (monthlyData.value?.stats?.expense_count || 0) + (monthlyData.value?.stats?.income_count || 0)
})

const currentMonthDisplay = computed(() => {
  if (!currentMonth.value) return '--'
  const [year, month] = currentMonth.value.split('-')
  return `${year}年${month}月`
})

const canGoPrev = computed(() => {
  const currentIndex = availableMonths.value.indexOf(currentMonth.value)
  return currentIndex < availableMonths.value.length - 1
})

const canGoNext = computed(() => {
  const currentIndex = availableMonths.value.indexOf(currentMonth.value)
  return currentIndex > 0
})

// 环比数据
const comparisons = computed(() => {
  return monthlyData.value?.stats?.comparisons || {}
})

// 获取环比显示数据
function getComparisonData(type) {
  // 月度分析页面的"交易情况"保持固定显示"与上月基本持平"
  if (type === 'count') {
    return {
      icon: 'fa-minus',
      iconClass: 'neutral',
      text: '与上月基本持平'
    }
  }

  const comp = comparisons.value[type]
  if (!comp) {
    return {
      icon: 'fa-minus',
      iconClass: 'neutral',
      text: '暂无对比数据'
    }
  }

  const { change, rate } = comp
  const threshold = 100 // 金额阈值100元

  if (change === null || change === undefined) {
    return {
      icon: 'fa-minus',
      iconClass: 'neutral',
      text: '暂无对比数据'
    }
  }

  if (Math.abs(change) < threshold) {
    return {
      icon: 'fa-minus',
      iconClass: 'neutral',
      text: '与上月基本持平'
    }
  }

  if (change > 0) {
    const unit = type === 'count' ? '笔' : '元'
    const amountText = type === 'count' ? Math.abs(change) : formatMoney(Math.abs(change))
    let text = `较上月增加 ${amountText} ${unit}`
    if (rate !== null && rate !== undefined) {
      text += ` (+${rate.toFixed(1)}%)`
    }
    return {
      icon: 'fa-arrow-up',
      iconClass: 'up',
      text
    }
  } else {
    const unit = type === 'count' ? '笔' : '元'
    const amountText = type === 'count' ? Math.abs(change) : formatMoney(Math.abs(change))
    let text = `较上月减少 ${amountText} ${unit}`
    if (rate !== null && rate !== undefined) {
      text += ` (${rate.toFixed(1)}%)`
    }
    return {
      icon: 'fa-arrow-down',
      iconClass: 'down',
      text
    }
  }
}

async function loadData(month) {
  console.log('[Monthly] loadData called with month:', month, 'currentMonth:', currentMonth.value, 'filter:', filterStore.currentFilter)

  if (month) {
    currentMonth.value = month
  } else if (!currentMonth.value && availableMonths.value.length > 0) {
    currentMonth.value = availableMonths.value[0]
    console.log('[Monthly] Set currentMonth to first available:', currentMonth.value)
  }

  if (!currentMonth.value) {
    console.warn('[Monthly] No current month available, skipping data load')
    return
  }

  try {
    const [year, monthNum] = currentMonth.value.split('-')
    console.log('[Monthly] Loading data for year:', year, 'month:', monthNum, 'with filter params:', filterStore.getFilterParams())
    uiStore.setGlobalLoading(true)

    // 组合参数：年份 + 月份 + 筛选条件
    const params = {
      year: year,
      month: monthNum,
      ...filterStore.getFilterParams()
    }

    const data = await dataStore.loadMonthlyData(params)
    console.log('[Monthly] Data loaded successfully:', data)

    monthlyData.value = data

    await nextTick()
    console.log('[Monthly] Initializing charts...')
    initCharts()
  } catch (error) {
    console.error('[Monthly] Failed to load data:', error)
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function prevMonth() {
  const currentIndex = availableMonths.value.indexOf(currentMonth.value)
  if (currentIndex < availableMonths.value.length - 1) {
    loadData(availableMonths.value[currentIndex + 1])
  }
}

function nextMonth() {
  const currentIndex = availableMonths.value.indexOf(currentMonth.value)
  if (currentIndex > 0) {
    loadData(availableMonths.value[currentIndex - 1])
  }
}

function switchType(type) {
  currentType.value = type
  updateCharts()
}

function initCharts() {
  if (!trendChartRef.value || !categoryPieChartRef.value) return

  // 初始化图表
  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
  }
  if (!categoryPieChart) {
    categoryPieChart = echarts.init(categoryPieChartRef.value)
  }

  updateCharts()

  // 响应式处理
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  trendChart?.resize()
  categoryPieChart?.resize()
}

function updateCharts() {
  if (!monthlyData.value) return

  initTrendChart()
  initCategoryChart()
}

function initTrendChart() {
  if (!trendChart) {
    console.warn('[Monthly] trendChart not initialized')
    return
  }
  if (!monthlyData.value) {
    console.warn('[Monthly] No monthlyData available for trend chart')
    return
  }

  const data = monthlyData.value || {}
  const dailyData = data.daily_data || { expense: { dates: [], amounts: [] }, income: { dates: [], amounts: [] } }
  const chartData = dailyData[currentType.value] || { dates: [], amounts: [] }

  console.log('[Monthly] Initializing trend chart with data:', { dailyData, chartData })

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>${currentType.value === 'expense' ? '支出' : '收入'}：${formatMoney(param.value)} 元`
      },
      axisPointer: {
        type: 'shadow'
      }
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
      data: chartData.dates || [],
      axisLabel: {
        fontSize: 12,
        color: 'var(--secondary-text)',
        formatter: (value) => {
          // 格式 "2024-01-15" -> "15"
          const parts = value.split('-')
          if (parts.length === 3) {
            return parts[2]
          }
          return value
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '金额 (元)',
      axisLabel: {
        fontSize: 12,
        color: 'var(--secondary-text)'
      }
    },
    series: [{
      name: currentType.value === 'expense' ? '支出' : '收入',
      type: 'bar',
      data: chartData.amounts || [],
      barMaxWidth: 50,
      barWidth: '60%',
      itemStyle: {
        color: currentType.value === 'expense' ? 'var(--danger-color)' : 'var(--success-color)',
        borderRadius: [4, 4, 0, 0]
      },
      emphasis: {
        itemStyle: {
          color: currentType.value === 'expense' ? 'var(--danger-color)' : 'var(--success-color)',
          opacity: 0.8
        },
        focus: 'series'
      },
      label: {
        show: false
      }
    }]
  }

  trendChart.setOption(option, true)

  // 绑定点击事件 - 查看当天交易明细
  trendChart.off('click')
  trendChart.on('click', (params) => {
    if (params.componentType === 'series') {
      const date = params.name
      console.log('[Monthly] Clicked on date:', date)
      // 这里可以打开交易明细模态框或跳转到交易页面
      // TODO: 实现点击查看明细功能
    }
  })
}

function initCategoryChart() {
  if (!categoryPieChart) {
    console.warn('[Monthly] categoryPieChart not initialized')
    return
  }
  if (!monthlyData.value) {
    console.warn('[Monthly] No monthlyData available for category chart')
    return
  }

  const data = monthlyData.value || {}
  // 使用 categories_source 来区分支付宝和微信
  const sourceData = data.categories_source || { expense: [], income: [] }
  const categorySourceData = sourceData[currentType.value] || []

  console.log('[Monthly] Initializing category chart with source data:', { sourceData, categorySourceData })

  // 计算总金额
  const total = categorySourceData.reduce((sum, item) => sum + item['金额'], 0)

  // 创建饼图数据，使用 "分类名-来源" 作为唯一名称
  const pieData = categorySourceData.map(item => {
    const uniqueName = `${item['交易分类']}-${item['来源']}`
    const percent = (item['金额'] / total * 100)
    return {
      name: uniqueName,
      value: item['金额'],
      originalName: item['交易分类'],
      source: item['来源'],
      itemStyle: {
        color: getCategoryColor(item['交易分类'])
      },
      label: {
        show: percent > 1 // 大于1%才显示标签
      },
      labelLine: {
        show: percent > 1
      }
    }
  }).sort((a, b) => b.value - a.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percent = ((params.value / total) * 100).toFixed(2)
        return `${params.data.originalName} (${params.data.source})<br/>金额：${formatMoney(params.value)} 元<br/>占比：${percent}%`
      }
    },
    legend: {
      show: false
    },
    series: [{
      name: currentType.value === 'expense' ? '支出分类' : '收入分类',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 4,
        borderWidth: 2,
        borderColor: '#fff'
      },
      label: {
        show: true,
        position: 'outside',
        formatter: (params) => {
          const percent = ((params.value / total) * 100).toFixed(2)
          return `${params.data.originalName}\n${percent}%`
        },
        fontSize: 12,
        color: '#666',
        lineHeight: 16
      },
      labelLine: {
        show: true,
        length: 15,
        length2: 10,
        smooth: true
      },
      data: pieData
    }]
  }

  categoryPieChart.setOption(option, true)

  // 绑定鼠标事件以高亮图例
  categoryPieChart.off('mouseover')
  categoryPieChart.off('mouseout')

  categoryPieChart.on('mouseover', (params) => {
    if (params.componentType === 'series') {
      const uniqueName = params.name
      const legendItem = document.querySelector(`.legend-item[data-unique-name="${uniqueName}"]`)
      if (legendItem) {
        legendItem.style.background = 'var(--hover-bg)'
        legendItem.style.fontWeight = '600'
      }
    }
  })

  categoryPieChart.on('mouseout', (params) => {
    if (params.componentType === 'series') {
      const uniqueName = params.name
      const legendItem = document.querySelector(`.legend-item[data-unique-name="${uniqueName}"]`)
      if (legendItem) {
        legendItem.style.background = 'transparent'
        legendItem.style.fontWeight = 'normal'
      }
    }
  })

  renderCustomLegend(categorySourceData, total)
}

function renderCustomLegend(categorySourceData, totalAmount) {
  if (!customLegendRef.value) return

  const container = customLegendRef.value
  container.innerHTML = ''

  container.style.display = 'flex'
  container.style.flexDirection = 'row'
  container.style.alignItems = 'flex-start'
  container.style.gap = '15px'

  // 分组数据：支付宝和微信
  const alipayData = categorySourceData
    .filter(item => item['来源'] === '支付宝')
    .sort((a, b) => b['金额'] - a['金额'])
  const wechatData = categorySourceData
    .filter(item => item['来源'] === '微信' || item['来源'] === 'wechat')
    .sort((a, b) => b['金额'] - a['金额'])

  // 创建分区块函数
  const createSection = (title, items, isTwoCol) => {
    if (items.length === 0) return null

    const section = document.createElement('div')
    section.className = 'legend-section'
    section.style.flex = isTwoCol ? '2' : '1'

    const header = document.createElement('h4')
    header.style.marginBottom = '10px'
    header.style.color = 'var(--text-color)'
    header.style.fontSize = '13px'
    header.style.fontWeight = '600'
    header.innerHTML = `<i class="fab fa-${title === '支付宝' ? 'alipay' : 'weixin'}" style="color: ${title === '支付宝' ? '#1677FF' : '#07C160'}; margin-right: 6px;"></i>${title} (${items.length})`
    section.appendChild(header)

    const list = document.createElement('div')
    list.style.display = 'grid'
    list.style.gridTemplateColumns = isTwoCol ? '1fr 1fr' : '1fr'
    list.style.gap = '6px 12px'

    items.forEach(item => {
      const percent = ((item['金额'] / totalAmount) * 100).toFixed(2)
      const uniqueName = `${item['交易分类']}-${item['来源']}`

      const itemDiv = document.createElement('div')
      itemDiv.className = 'legend-item'
      itemDiv.setAttribute('data-unique-name', uniqueName)
      itemDiv.style.display = 'flex'
      itemDiv.style.alignItems = 'center'
      itemDiv.style.cursor = 'pointer'
      itemDiv.style.fontSize = '14px'
      itemDiv.style.padding = '3px 4px'
      itemDiv.style.borderRadius = '4px'
      itemDiv.style.transition = 'all 0.2s'

      itemDiv.onmouseover = () => {
        itemDiv.style.background = 'var(--hover-bg)'
        categoryPieChart.dispatchAction({
          type: 'highlight',
          name: uniqueName
        })
      }

      itemDiv.onmouseout = () => {
        itemDiv.style.background = 'transparent'
        categoryPieChart.dispatchAction({
          type: 'downplay',
          name: uniqueName
        })
      }

      // 颜色点
      const dot = document.createElement('span')
      dot.style.width = '10px'
      dot.style.height = '10px'
      dot.style.borderRadius = '50%'
      dot.style.backgroundColor = getCategoryColor(item['交易分类'])
      dot.style.marginRight = '8px'
      dot.style.flexShrink = '0'

      // 文本
      const text = document.createElement('div')
      text.style.flex = '1'
      text.style.display = 'flex'
      text.style.justifyContent = 'flex-start'
      text.style.alignItems = 'baseline'
      text.style.whiteSpace = 'nowrap'

      const nameSpan = document.createElement('span')
      nameSpan.textContent = item['交易分类']
      nameSpan.style.fontWeight = '500'
      nameSpan.style.marginRight = '4px'

      const percentSpan = document.createElement('span')
      percentSpan.textContent = `${percent}%`
      percentSpan.style.color = 'var(--secondary-text)'
      percentSpan.style.fontSize = '0.9em'

      text.appendChild(nameSpan)
      text.appendChild(percentSpan)

      itemDiv.appendChild(dot)
      itemDiv.appendChild(text)
      list.appendChild(itemDiv)
    })

    section.appendChild(list)
    return section
  }

  // 添加支付宝区块（两列布局）
  if (alipayData.length > 0) {
    const alipaySection = createSection('支付宝', alipayData, true)
    if (alipaySection) container.appendChild(alipaySection)
  }

  // 添加微信区块（单列布局）
  if (wechatData.length > 0) {
    const wechatSection = createSection('微信', wechatData, false)
    if (wechatSection) container.appendChild(wechatSection)
  }
}

// 监听筛选器变化，重新加载数据
watch(() => filterStore.currentFilter, (newFilter, oldFilter) => {
  console.log('[Monthly] Filter changed from', oldFilter, 'to', newFilter)
  if (currentMonth.value) {
    console.log('[Monthly] Reloading data due to filter change')
    loadData(currentMonth.value)
  }
})

onMounted(async () => {
  try {
    uiStore.setGlobalLoading(true)

    // 加载可用日期（包含月份列表）
    await dataStore.loadAvailableDates()
    availableMonths.value = dataStore.availableDates?.months || []
    console.log('[Monthly] Available months:', availableMonths.value)

    if (availableMonths.value.length > 0) {
      // 如果进入演示模式，稍作延迟以确保数据已准备好
      if (sessionStore.isDemo) {
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      // 现在加载数据
      await loadData()
    }
  } catch (error) {
    console.error('Monthly page init error:', error)
    uiStore.showError('页面初始化失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  categoryPieChart?.dispose()
})
</script>

<style scoped>
.monthly-page {
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
  min-width: 100px;
  text-align: center;
}

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
  margin-bottom: 12px;
}

.stat-card .comparison {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}

.trend-icon {
  font-size: 12px;
}

.trend-icon.up {
  color: var(--success-color);
}

.trend-icon.down {
  color: var(--danger-color);
}

.trend-icon.neutral {
  color: var(--secondary-text);
}

.card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.chart-toggle {
  display: flex;
  gap: 8px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-color);
}

.toggle-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.toggle-btn:hover:not(.active) {
  background: var(--hover-bg);
}

.chart-container {
  height: 400px;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
