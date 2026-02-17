<template>
  <div class="insights-page">
    <div class="page-header">
      <h1 class="page-title">消费洞察</h1>
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

    <div v-if="uiStore.globalLoading && !insightsData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="insightsData" class="insights-content">
      <!-- 顶部区域：桑基图 + 年度故事 -->
      <div class="top-analysis-section">
        <!-- 桑基图 -->
        <div class="analysis-card sankey-card">
          <div class="card-header">
            <h2 class="card-title">资金流向全景</h2>
          </div>
          <div class="card-content" ref="sankeyChartRef"></div>
        </div>

        <!-- 年度故事 -->
        <div class="analysis-card story-entry-card" @click="showStoryModeFunc">
          <div class="story-card-content">
            <div class="story-icon">
              <i class="fas fa-film"></i>
            </div>
            <div class="story-title">年度消费故事</div>
            <div class="story-desc">点击开启您的时光之旅</div>
            <div class="story-btn">立即播放</div>
          </div>
        </div>
      </div>

      <!-- 核心分析网格 -->
      <div class="core-analysis-grid">
        <!-- 消费画像 -->
        <div class="analysis-card profile-card">
          <div class="card-header">
            <h2 class="card-title">消费画像</h2>
          </div>
          <div class="card-content profile-content" ref="profileContent">
            <!-- 动态内容 -->
          </div>
        </div>

        <!-- 最常光顾 -->
        <div class="analysis-card merchant-list-card">
          <div class="card-header">
            <h2 class="card-title">最常光顾</h2>
          </div>
          <div class="card-content">
            <div class="merchant-list" ref="merchantList">
              <!-- 动态内容 -->
            </div>
          </div>
        </div>

        <!-- 消费场景 -->
        <div class="analysis-card scenario-card">
          <div class="card-header">
            <h2 class="card-title">消费场景</h2>
          </div>
          <div class="card-content">
            <div class="scenario-tabs">
              <button class="tab-btn" :class="{ active: currentScenario === 'channel' }" @click="setScenario('channel')">消费渠道</button>
              <button class="tab-btn" :class="{ active: currentScenario === 'time' }" @click="setScenario('time')">时段分布</button>
              <button class="tab-btn" :class="{ active: currentScenario === 'amount' }" @click="setScenario('amount')">金额层级</button>
              <button class="tab-btn" :class="{ active: currentScenario === 'payment' }" @click="setScenario('payment')">支付方式</button>
            </div>
            <div ref="scenarioChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- 消费习惯 -->
        <div class="analysis-card habit-card">
          <div class="card-header">
            <h2 class="card-title">消费习惯</h2>
          </div>
          <div class="card-content">
            <div class="habit-stats" ref="habitStats">
              <!-- 动态内容 -->
            </div>
          </div>
        </div>
      </div>

      <!-- 高级洞察网格 -->
      <div class="advanced-insights-grid">
        <!-- 拿铁因子 -->
        <div class="analysis-card insight-card latte-card">
          <div class="card-header">
            <h2 class="card-title">拿铁因子</h2>
          </div>
          <div class="card-content" ref="latteContent"></div>
        </div>

        <!-- 隐形订阅 -->
        <div class="analysis-card insight-card sub-card">
          <div class="card-header">
            <h2 class="card-title">隐形订阅</h2>
          </div>
          <div class="card-content" ref="subContent"></div>
        </div>

        <!-- 个人通胀 -->
        <div class="analysis-card insight-card inflation-card">
          <div class="card-header">
            <h2 class="card-title">消费通胀</h2>
          </div>
          <div class="card-content" ref="inflationContent"></div>
        </div>

        <!-- 品牌忠诚度 -->
        <div class="analysis-card insight-card loyalty-card">
          <div class="card-header">
            <h2 class="card-title">品牌忠诚</h2>
          </div>
          <div class="card-content" ref="loyaltyContent"></div>
        </div>

        <!-- 周末效应 -->
        <div class="analysis-card insight-card weekend-card">
          <div class="card-header">
            <h2 class="card-title">周末效应</h2>
          </div>
          <div class="card-content" ref="weekendContent"></div>
        </div>
      </div>

      <!-- 高级可视化图表区域 -->
      <div class="advanced-viz-section">
        <h2 class="section-title">深度洞察</h2>

        <!-- 时间密码 -->
        <div class="viz-section-header">
          <div class="section-subtitle"><i class="fas fa-clock"></i> 时间密码</div>
        </div>

        <!-- 河流图 -->
        <div class="analysis-card full-width-viz-card">
          <div class="card-header">
            <h2 class="card-title">消费趋势河流</h2>
          </div>
          <div class="card-content" ref="themeRiverChartRef"></div>
        </div>

        <!-- 热力图 + 雷达图 -->
        <div class="viz-row">
          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">消费生物钟 (热力图)</h2>
            </div>
            <div class="card-content" ref="heatmapChartRef"></div>
          </div>

          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">季度消费结构</h2>
            </div>
            <div class="card-content" ref="radarChartRef"></div>
          </div>
        </div>

        <!-- 决策心理 -->
        <div class="viz-section-header">
          <div class="section-subtitle"><i class="fas fa-brain"></i> 决策心理</div>
        </div>

        <!-- 象限图 -->
        <div class="analysis-card full-width-viz-card" style="height: 600px;">
          <div class="card-header">
            <h2 class="card-title">消费象限 (频次 vs 均价)</h2>
          </div>
          <div class="card-content" ref="quadrantChartRef"></div>
        </div>

        <!-- 和弦图 + 漏斗图 -->
        <div class="viz-row">
          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">消费关联和弦</h2>
            </div>
            <div class="card-content" ref="chordChartRef"></div>
          </div>

          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">消费金额漏斗</h2>
            </div>
            <div class="card-content" ref="funnelChartRef"></div>
          </div>
        </div>

        <!-- 结构解析 -->
        <div class="viz-section-header">
          <div class="section-subtitle"><i class="fas fa-chart-pie"></i> 结构解析</div>
        </div>

        <!-- 帕累托图 -->
        <div class="analysis-card full-width-viz-card">
          <div class="card-header">
            <h2 class="card-title">核心支出来源 (帕累托图)</h2>
          </div>
          <div class="card-content" ref="paretoChartRef" style="height: 400px;"></div>
        </div>

        <!-- 词云图 + 箱形图 -->
        <div class="viz-row">
          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">消费热词云</h2>
            </div>
            <div class="card-content" ref="wordCloudChartRef"></div>
          </div>

          <div class="analysis-card">
            <div class="card-header">
              <h2 class="card-title">消费分布云图</h2>
            </div>
            <div class="card-content" ref="boxPlotChartRef"></div>
          </div>
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

    <!-- 时光机 Modal -->
    <div v-if="showStoryMode" class="story-modal" @click.self="showStoryMode = false" style="display: flex;">
      <div class="story-content">
        <button class="close-story" @click="showStoryMode = false">
          <i class="fas fa-times"></i>
        </button>
        <div class="story-slides" ref="storySlides">
          <!-- 动态生成幻灯片 -->
        </div>
        <div class="story-controls">
          <button class="story-btn prev" @click="prevSlide">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="story-indicators" ref="storyIndicators"></div>
          <button class="story-btn next" @click="nextSlide">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
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
import 'echarts-wordcloud'
import api from '@/api/client'

const dataStore = useDataStore()
const uiStore = useUiStore()
const sessionStore = useSessionStore()
const filterStore = useFilterStore()

// 状态
const currentYear = ref(new Date().getFullYear())
const availableYears = ref([])
const insightsData = ref(null)
const currentScenario = ref('channel')
const showStoryMode = ref(false)
const currentSlide = ref(0)

// 图表引用
const sankeyChartRef = ref(null)
const scenarioChartRef = ref(null)
const themeRiverChartRef = ref(null)
const heatmapChartRef = ref(null)
const radarChartRef = ref(null)
const quadrantChartRef = ref(null)
const chordChartRef = ref(null)
const funnelChartRef = ref(null)
const paretoChartRef = ref(null)
const wordCloudChartRef = ref(null)
const boxPlotChartRef = ref(null)

// DOM引用
const profileContent = ref(null)
const merchantList = ref(null)
const habitStats = ref(null)
const latteContent = ref(null)
const subContent = ref(null)
const inflationContent = ref(null)
const loyaltyContent = ref(null)
const weekendContent = ref(null)
const storySlides = ref(null)
const storyIndicators = ref(null)

// 图表实例
let scenarioChart = null
let themeRiverChart = null
let heatmapChart = null
let radarChart = null
let quadrantChart = null
let chordChart = null
let funnelChart = null
let paretoChart = null
let wordCloudChart = null
let boxPlotChart = null
let sankeyChart = null

// 计算属性
const canGoPrev = computed(() => {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  return currentIndex < availableYears.value.length - 1
})

const canGoNext = computed(() => {
  const currentIndex = availableYears.value.indexOf(currentYear.value)
  return currentIndex > 0
})

const storyData = computed(() => {
  return insightsData.value?.story_data || []
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

function setScenario(type) {
  currentScenario.value = type
  updateScenarioChart()
}

function prevSlide() {
  if (currentSlide.value > 0) {
    currentSlide.value--
    updateSlidePosition()
  }
}

function nextSlide() {
  if (currentSlide.value < totalSlides - 1) {
    currentSlide.value++
    updateSlidePosition()
  }
}

function updateSlidePosition() {
  const slides = storySlides.value
  if (slides) {
    const allSlides = slides.querySelectorAll('.slide')
    allSlides.forEach((slide, index) => {
      slide.classList.toggle('active', index === currentSlide.value)
    })
    updateIndicators()
  }
}

function updateIndicators() {
  const indicators = storyIndicators.value
  if (indicators) {
    Array.from(indicators.children).forEach((dot, index) => {
      dot.classList.toggle('active', index === currentSlide.value)
    })
  }
}

// 故事模式相关
let totalSlides = 0

async function showStoryModeFunc() {
  const data = storyData.value
  if (!data) {
    console.warn('[Story] No story data available')
    return
  }

  currentSlide.value = 0
  showStoryMode.value = true

  // 等待 DOM 更新后再生成幻灯片
  await nextTick()
  generateStorySlides()
}

function generateStorySlides() {
  const data = storyData.value
  console.log('[Story] generateStorySlides called, data:', data)

  if (!data) {
    console.warn('[Story] No data available')
    return
  }

  const slides = storySlides.value
  const indicators = storyIndicators.value

  console.log('[Story] slides element:', slides)
  console.log('[Story] indicators element:', indicators)

  if (!slides || !indicators) {
    console.warn('[Story] DOM elements not found')
    return
  }

  // 生成幻灯片（与老前端保持一致的模板）
  const slideTemplates = [
    // 1. 封面
    `
    <div class="slide active">
      <div class="slide-content">
        <h1>您的年度消费故事</h1>
        <p>这一年，您经历了 ${data.summary.total_days} 个日夜</p>
        <p>完成了 ${data.summary.tx_count} 笔交易</p>
        <div class="slide-big-icon"><i class="fas fa-book-open"></i></div>
      </div>
    </div>
    `,
    // 2. 年度首单
    (data.features && data.features.first_tx) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>🎬 故事的开始</h2>
        <div class="slide-date">${data.features.first_tx.date}</div>
        <p>您在 <strong>${data.features.first_tx.merchant}</strong></p>
        <div class="slide-amount">¥${formatMoney(data.features.first_tx.amount)}</div>
        <p>用这笔消费开启了全新的一年。</p>
        <div class="slide-big-icon"><i class="fas fa-play-circle"></i></div>
      </div>
    </div>
    ` : '',
    // 3. 黄金时间
    (data.features && data.features.peak_hour !== undefined) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>⏰ 剁手黄金点</h2>
        <p>每天的 <strong>${data.features.peak_hour}点</strong></p>
        <div class="slide-keyword" style="font-size:32px">是您最活跃的时刻</div>
        <p>${data.features.peak_hour < 12 ? '早起的鸟儿有虫吃？' : (data.features.peak_hour > 20 ? '月黑风高夜，正是剁手时。' : '工作日摸鱼下单？')}</p>
        <div class="slide-big-icon"><i class="fas fa-clock"></i></div>
      </div>
    </div>
    ` : '',
    // 4. 外卖之王
    (data.features && data.features.takeout && data.features.takeout.count > 5) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>🥡 外卖品鉴家</h2>
        <div class="slide-amount">${data.features.takeout.count} 单</div>
        <p>贡献了 ${formatMoney(data.features.takeout.amount)} 元给外卖/快餐</p>
        <p>世界那么大，还是外卖最懂你的胃。</p>
        <div class="slide-big-icon"><i class="fas fa-utensils"></i></div>
      </div>
    </div>
    ` : '',
    // 5. 季节限定
    (data.features && data.features.top_season) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>🍂 季节限定记忆</h2>
        <p>您在</p>
        <div class="slide-keyword" style="color:#FF7950">${data.features.top_season}天</div>
        <p>留下了最多的消费足迹。</p>
        <div class="slide-big-icon"><i class="fas ${data.features.top_season === '冬' ? 'fa-snowflake' : (data.features.top_season === '夏' ? 'fa-sun' : 'fa-leaf')}"></i></div>
      </div>
    </div>
    ` : '',
    // 6. 咖啡/奶茶指数
    (data.features && data.features.coffee && data.features.coffee.count > 0) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>☕️ 续命指数</h2>
        <div class="slide-amount">${data.features.coffee.count} 杯</div>
        <p>您今年在咖啡/奶茶上投入了</p>
        <div class="slide-keyword" style="font-size:24px">¥${formatMoney(data.features.coffee.amount)}</div>
        <p>${data.features.coffee.count > 100 ? '相当于喝掉了一个浴缸的量！' : '您是理性的咖啡因摄入者。'}</p>
        <div class="slide-big-icon"><i class="fas fa-coffee"></i></div>
      </div>
    </div>
    ` : '',
    // 7. 深夜哲学
    (data.features && data.features.night && data.features.night.count > 0) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>🌙 深夜哲学</h2>
        <p>晚10点后，您平均消费</p>
        <div class="slide-amount">¥${formatMoney(data.features.night.avg)}</div>
        <p>看来深夜不仅有灵感，还有食欲。</p>
        <div class="slide-big-icon"><i class="fas fa-moon"></i></div>
      </div>
    </div>
    ` : '',
    // 8. 周末人格
    (data.features && data.features.weekend) ? `
    <div class="slide">
      <div class="slide-content">
        <h2>🎭 周末人格</h2>
        <p>工作日均价 vs 周末均价</p>
        <div class="slide-amount" style="font-size:32px">¥${formatMoney(data.features.weekend.weekday_avg)} <span style="font-size:20px;color:#999">vs</span> ¥${formatMoney(data.features.weekend.weekend_avg)}</div>
        <p>${data.features.weekend.weekend_avg > data.features.weekend.weekday_avg * 2 ? '平日沙县小吃，周末米其林大餐！' : '您的消费习惯非常稳定。'}</p>
        <div class="slide-big-icon"><i class="fas fa-mask"></i></div>
      </div>
    </div>
    ` : '',
    // 9. 通胀感知
    (data.features && data.features.inflation && data.features.inflation.trend !== 'stable') ? `
    <div class="slide">
      <div class="slide-content">
        <h2>📈 通胀感知</h2>
        <p>您常去的 <strong>${data.features.inflation.merchant}</strong></p>
        <div class="slide-amount" style="font-size:32px">¥${formatMoney(data.features.inflation.start_price)} ➔ ¥${formatMoney(data.features.inflation.end_price)}</div>
        <p>${data.features.inflation.trend === 'up' ? '悄悄涨价了，且喝且珍惜。' : '居然降价了？良心商家！'}</p>
        <div class="slide-big-icon"><i class="fas fa-chart-line"></i></div>
      </div>
    </div>
    ` : '',
    // 10. 最贵的一天
    `
    <div class="slide">
      <div class="slide-content">
        <h2>💸 最"壕"的一天</h2>
        <div class="slide-date">${data.max_day.date}</div>
        <div class="slide-amount">${formatMoney(data.max_day.amount)}</div>
        <p>那天发生了什么？是爱自己多一点吗？</p>
        <div class="slide-big-icon"><i class="fas fa-shopping-bag"></i></div>
      </div>
    </div>
    `,
    // 11. 总结
    `
    <div class="slide">
      <div class="slide-content">
        <h2>✨ 年度关键词</h2>
        <div class="slide-keyword">${data.top_category.name}</div>
        <p>这是您投入最多的领域 (${formatMoney(data.top_category.amount)})</p>
        <p>新的一年，愿每一笔消费都物超所值！</p>
        <div class="slide-big-icon"><i class="fas fa-star"></i></div>
      </div>
    </div>
    `
  ].filter(Boolean) // 过滤掉空字符串（条件为false的幻灯片）

  totalSlides = slideTemplates.length

  // 设置幻灯片内容
  slides.innerHTML = slideTemplates.join('')

  // 生成指示器
  indicators.innerHTML = slideTemplates.map((_, i) =>
    `<span class="indicator ${i === 0 ? 'active' : ''}" data-slide-index="${i}"></span>`
  ).join('')

  // 更新幻灯片位置
  updateSlidePosition()
}

async function loadData(year) {
  try {
    console.log('[Insights] Loading data for year:', year, 'filter:', filterStore.currentFilter)
    uiStore.setGlobalLoading(true)

    const params = {
      year: year,
      ...filterStore.getFilterParams()
    }

    const data = await api.getAnalysis(params)
    console.log('[Insights] Data loaded:', data)

    insightsData.value = data

    await nextTick()
    initCharts()
    updateAllContent()
  } catch (error) {
    console.error('[Insights] Failed to load data:', error)
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
}

function initCharts() {
  if (scenarioChartRef.value) {
    scenarioChart = echarts.init(scenarioChartRef.value)
  }
  if (themeRiverChartRef.value) {
    themeRiverChart = echarts.init(themeRiverChartRef.value)
  }
  if (heatmapChartRef.value) {
    heatmapChart = echarts.init(heatmapChartRef.value)
  }
  if (radarChartRef.value) {
    radarChart = echarts.init(radarChartRef.value)
  }
  if (quadrantChartRef.value) {
    quadrantChart = echarts.init(quadrantChartRef.value)
  }
  if (chordChartRef.value) {
    chordChart = echarts.init(chordChartRef.value)
  }
  if (funnelChartRef.value) {
    funnelChart = echarts.init(funnelChartRef.value)
  }
  if (paretoChartRef.value) {
    paretoChart = echarts.init(paretoChartRef.value)
  }
  if (wordCloudChartRef.value) {
    wordCloudChart = echarts.init(wordCloudChartRef.value)
  }
  if (boxPlotChartRef.value) {
    boxPlotChart = echarts.init(boxPlotChartRef.value)
  }
  if (sankeyChartRef.value) {
    sankeyChart = echarts.init(sankeyChartRef.value)
  }

  updateScenarioChart()
  updateAdvancedCharts()

  window.addEventListener('resize', handleResize)
}

function handleResize() {
  scenarioChart?.resize()
  themeRiverChart?.resize()
  heatmapChart?.resize()
  radarChart?.resize()
  quadrantChart?.resize()
  chordChart?.resize()
  funnelChart?.resize()
  paretoChart?.resize()
  wordCloudChart?.resize()
  boxPlotChart?.resize()
  sankeyChart?.resize()
}

function updateAllContent() {
  updateTags()
  updateMerchants()
  updateHabitStats()
  updateAdvancedInsights()
}

function updateTags() {
  const data = insightsData.value
  if (!data || !profileContent.value) return

  // 后端返回的 tags 是一个对象，包含 tags 数组和其他特征字段
  const tagsData = data.tags || {}
  const tags = tagsData.tags || []

  const tagsHtml = `
    <div class="tag-cloud">
      ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
    </div>
  `

  const detailsHtml = `
    <div class="profile-details">
      <div class="profile-feature">
        <div class="feature-icon"><i class="fas fa-clock"></i></div>
        <div class="feature-content">
          <div class="feature-title">消费时间</div>
          <div class="feature-description">${formatTimePattern(tagsData.time_pattern || '-')}</div>
        </div>
      </div>
      <div class="profile-feature">
        <div class="feature-icon"><i class="fas fa-shopping-bag"></i></div>
        <div class="feature-content">
          <div class="feature-title">消费偏好</div>
          <div class="feature-description">${formatPreference(tagsData.spending_preference || '-')}</div>
        </div>
      </div>
      <div class="profile-feature">
        <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
        <div class="feature-content">
          <div class="feature-title">消费规律</div>
          <div class="feature-description">${formatPattern(tagsData.spending_pattern || '-')}</div>
        </div>
      </div>
      <div class="profile-feature">
        <div class="feature-icon"><i class="fas fa-wallet"></i></div>
        <div class="feature-content">
          <div class="feature-title">消费能力</div>
          <div class="feature-description">${formatPower(tagsData.spending_power || '-')}</div>
        </div>
      </div>
    </div>
  `

  profileContent.value.innerHTML = tagsHtml + detailsHtml
}

// 格式化函数（从老前端迁移）
function formatTimePattern(text) {
  if (text === '-') return text
  return text.replace(/(夜间|早起|日间)/g, '<span class="highlight">$1</span>')
}

function formatPreference(text) {
  if (text === '-') return text
  return text.replace(/最常消费的品类是/, '')
    .replace(/([^，。]+?)(\([0-9.]+%\))/g, '<span class="highlight">$1</span><span class="percentage">$2</span>')
}

function formatPattern(text) {
  if (text === '-') return text
  return text.replace(/(非常有规律|理性|较为均衡|比较随性)/g, '<span class="highlight">$1</span>')
}

function formatPower(text) {
  if (text === '-') return text
  return text.replace(
    /日均消费([0-9]+)元/g,
    '日均消费<span class="amount">$1</span>元'
  ).replace(
    /，属于(高|中等|理性)消费人群/g,
    '，属于<span class="highlight">$1</span>消费人群'
  )
}

function updateMerchants() {
  const data = insightsData.value
  if (!data || !merchantList.value) return

  const merchants = data.merchant_analysis?.frequent_merchants || []

  merchantList.value.innerHTML = merchants.map((merchant, index) => `
    <div class="merchant-item ${index < 3 ? 'top-' + (index + 1) : ''}">
      <div class="merchant-info">
        <div class="merchant-rank">${index + 1}</div>
        <div class="merchant-details">
          <div class="merchant-name">${merchant.name}</div>
          <div class="merchant-meta">上次消费: ${merchant.last_visit || '-'}</div>
        </div>
      </div>
      <div class="merchant-stats">
        <div class="stat-group">
          <div class="label">消费金额</div>
          <div class="value">${formatMoney(merchant.amount)}</div>
        </div>
        <div class="stat-group">
          <div class="label">消费次数</div>
          <div class="value">${merchant.count}次</div>
        </div>
      </div>
    </div>
  `).join('')
}

function updateScenarioChart() {
  if (!scenarioChart || !insightsData.value) return

  const scenarioData = insightsData.value.scenario_analysis || []
  const paymentData = insightsData.value.payment_analysis || []

  const groupedData = {
    'channel': scenarioData.filter(item => item.category === '渠道'),
    'time': scenarioData.filter(item => item.category === '时段'),
    'amount': scenarioData.filter(item => item.category === '层级'),
    'payment': paymentData.map(item => ({
      name: item.name,
      value: item.total_amount
    }))
  }

  const chartData = groupedData[currentScenario.value] || []
  const total = chartData.reduce((sum, item) => sum + (item.value || 0), 0)

  const colorSchemes = {
    channel: ['#007AFF', '#5856D6'],
    time: ['#FF9500', '#FF3B30', '#34C759', '#5856D6', '#007AFF', '#FF2D55'],
    amount: ['#FF3B30', '#FF9500', '#34C759', '#007AFF'],
    payment: ['#007AFF', '#FF9500', '#34C759', '#5856D6', '#FF3B30', '#FF2D55', '#64D2FF']
  }

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percentage = ((params.value / total) * 100).toFixed(2)
        return `${params.name}<br/>金额：${formatMoney(params.value)}元<br/>占比：${percentage}%`
      }
    },
    series: [{
      name: '金额分布',
      type: 'pie',
      radius: ['25%', '60%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 5,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'outside',
        formatter: (params) => {
          const percentage = ((params.value / total) * 100).toFixed(2)
          return percentage > 1 ? `${params.name}\n${percentage}%` : ''
        },
        fontSize: 12,
        color: '#666',
        lineHeight: 16
      },
      labelLine: {
        show: (params) => ((params.value / total) * 100) > 1,
        length: 8,
        length2: 8,
        smooth: true,
        maxSurfaceAngle: 80
      },
      data: chartData.map((item, index) => ({
        name: item.name,
        value: item.value,
        itemStyle: {
          color: colorSchemes[currentScenario.value][index % colorSchemes[currentScenario.value].length]
        }
      }))
    }]
  }

  scenarioChart.setOption(option, true)
}

function updateHabitStats() {
  const data = insightsData.value
  if (!data || !habitStats.value) return

  const habit = data.habit_analysis || {}
  const night = data.nighttime_analysis || {}
  const engel = data.engel_coefficient || {}

  habitStats.value.innerHTML = `
    <div class="stat-item">
      <div class="stat-value">${habit.daily_avg?.toFixed(2) || 0}</div>
      <div class="stat-label">日均消费(元)</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${habit.weekend_ratio || 0}%</div>
      <div class="stat-label">周末消费占比</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${habit.fixed_expenses || 0}%</div>
      <div class="stat-label">固定支出占比</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${habit.month_start_ratio || 0}%</div>
      <div class="stat-label">月初消费占比</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${night.ratio?.toFixed(2) || 0}%</div>
      <div class="stat-label">深夜剁手</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${engel.ratio?.toFixed(2) || 0}%</div>
      <div class="stat-label">恩格尔系数</div>
    </div>
  `
}

function updateAdvancedInsights() {
  const data = insightsData.value
  if (!data) return

  // 拿铁因子
  const latte = data.latte_factor || {}
  if (latteContent.value) {
    latteContent.value.innerHTML = `
      <div class="insight-stat-big">${formatMoney(latte.total_amount || 0)}</div>
      <div class="insight-desc">累计在 <span class="highlight">${latte.top_merchant || '-'}</span> 等小额消费上花费</div>
      <div class="insight-meta">相当于 ${Math.floor((latte.total_amount || 0) / 30)} 杯咖啡</div>
    `
  }

  // 隐形订阅
  const subs = data.subscription_analysis || []
  if (subContent.value) {
    if (subs.length > 0) {
      const totalAnnual = subs.reduce((sum, item) => sum + (item.annual_amount || 0), 0)
      subContent.value.innerHTML = `
        <div class="insight-stat-big">${formatMoney(totalAnnual)}</div>
        <div class="insight-desc">预估年化订阅总支出</div>
        <div class="insight-list">
          ${subs.slice(0, 2).map(s => `
            <div class="insight-item">
              <span>${s.name}</span>
              <span>${formatMoney(s.monthly_amount)}/月</span>
            </div>
          `).join('')}
        </div>
      `
    } else {
      subContent.value.innerHTML = `<div class="empty-state">未发现明显订阅支出</div>`
    }
  }

  // 个人通胀
  const inf = data.inflation_analysis || {}
  if (inflationContent.value) {
    const trendIcon = inf.trend === 'up' ? 'fa-arrow-up' : (inf.trend === 'down' ? 'fa-arrow-down' : 'fa-minus')
    const trendColor = inf.trend === 'up' ? '#FF3B30' : (inf.trend === 'down' ? '#34C759' : '#8E8E93')
    inflationContent.value.innerHTML = `
      <div class="insight-stat-big" style="color: ${trendColor}">
        <i class="fas ${trendIcon}"></i> ${Math.abs(inf.rate || 0).toFixed(2)}%
      </div>
      <div class="insight-desc">季度客单价变化趋势</div>
      <div class="insight-meta">从 ${formatMoney(inf.first_avg || 0)} 变动至 ${formatMoney(inf.last_avg || 0)}</div>
    `
  }

  // 品牌忠诚度
  const loyalty = data.brand_loyalty || {}
  if (loyaltyContent.value && loyalty.top_amount) {
    loyaltyContent.value.innerHTML = `
      <div class="loyalty-row">
        <div class="loyalty-item">
          <div class="loyalty-value">${loyalty.top_amount.name || '-'}</div>
          <div class="loyalty-details">
            <span class="loyalty-amount">${formatMoney(loyalty.top_amount.value || 0)}</span>
            <span class="loyalty-tag">真金白银</span>
          </div>
        </div>
        <div class="loyalty-item">
          <div class="loyalty-value">${loyalty.top_count?.name || '-'}</div>
          <div class="loyalty-details">
            <span class="loyalty-amount">${loyalty.top_count.value || 0}次</span>
            <span class="loyalty-tag">最为长情</span>
          </div>
        </div>
      </div>
    `
  }

  // 周末效应
  const wm = data.weekend_monday || {}
  if (weekendContent.value) {
    const wmRatio = wm.ratio || 0
    let wmDesc = "平稳型"
    if (wmRatio > 1.5) wmDesc = "周末狂欢型"
    else if (wmRatio < 0.8) wmDesc = "周一补偿型"

    weekendContent.value.innerHTML = `
      <div class="insight-stat-big">${wmRatio.toFixed(2)}x</div>
      <div class="insight-desc">周末日均消费是周一的倍数</div>
      <div class="insight-meta">类型: ${wmDesc}</div>
    `
  }
}

function updateAdvancedCharts() {
  const data = insightsData.value
  if (!data) return

  // 桑基图
  if (data.sankey_data && sankeyChart) {
    renderSankeyChart(data.sankey_data)
  }

  // 河流图
  if (data.themeriver_data && themeRiverChart) {
    renderThemeRiver(data.themeriver_data)
  }

  // 箱形图
  if (data.boxplot_data && boxPlotChart) {
    renderBoxPlot(data.boxplot_data)
  }

  // 热力图
  if (data.heatmap_data && heatmapChart) {
    renderHeatmap(data.heatmap_data)
  }

  // 帕累托图
  if (data.pareto_data && paretoChart) {
    renderParetoChart(data.pareto_data)
  }

  // 和弦图
  if (data.chord_data && chordChart) {
    renderChordChart(data.chord_data)
  }

  // 象限图
  if (data.quadrant_data && quadrantChart) {
    renderQuadrantChart(data.quadrant_data)
  }

  // 漏斗图
  if (data.funnel_data && funnelChart) {
    renderFunnelChart(data.funnel_data)
  }

  // 雷达图
  if (data.radar_data && radarChart) {
    renderRadarChart(data.radar_data)
  }

  // 词云图
  if (data.wordcloud_data && wordCloudChart) {
    renderWordCloud(data.wordcloud_data)
  }
}

function renderSankeyChart(data) {
  if (!sankeyChart || !data.nodes || data.nodes.length === 0) return

  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      formatter: function (params) {
        if (params.dataType === 'edge') {
          return `${params.data.source} > ${params.data.target}<br/>金额: ${formatMoney(params.data.value)} 元`
        } else {
          return `${params.name}<br/>金额: ${formatMoney(params.data.value || params.value)} 元`
        }
      }
    },
    series: [{
      type: 'sankey',
      layoutIterations: 0,  // 禁止自动优化布局，严格按照数据顺序排列，避免连线交叉
      nodeGap: 12,          // 增加节点间距
      data: data.nodes,
      links: data.links,
      emphasis: {
        focus: 'adjacency'
      },
      lineStyle: {
        color: 'gradient',
        curveness: 0.5
      },
      label: {
        color: 'rgba(0,0,0,0.7)',
        fontFamily: 'Arial'
      }
    }]
  }

  sankeyChart.setOption(option, true)
}

function renderThemeRiver(data) {
  if (!themeRiverChart || !data.data || data.data.length === 0) return

  const themeRiverData = data.data.map(item => [item[0], item[2], item[1]])
  const colors = data.categories.map(cat => getCategoryColor(cat))

  const option = {
    color: colors,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: 'rgba(0,0,0,0.2)',
          width: 1,
          type: 'solid'
        }
      },
      formatter: (params) => {
        if (!params || params.length === 0) return ''
        const date = new Date(params[0].axisValue)
        const dateStr = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0')

        let result = '<div style="font-weight:bold;margin-bottom:5px;">' + dateStr + '</div>'
        const sortedParams = [...params].sort((a, b) => b.value[1] - a.value[1])

        sortedParams.forEach(item => {
          const name = item.value[2]
          const value = item.value[1]
          result += '<div style="display:flex;justify-content:space-between;align-items:center;min-width:150px;">' +
            '<span>' + item.marker + ' ' + name + '</span>' +
            '<span style="font-weight:bold;margin-left:15px;">¥' + formatMoney(value) + '</span>' +
            '</div>'
        })
        return result
      }
    },
    legend: {
      data: data.categories,
      top: 10,
      textStyle: {
        fontSize: 12
      }
    },
    singleAxis: {
      top: 50,
      bottom: 50,
      axisTick: {},
      axisLabel: {},
      type: 'time',
      axisPointer: {
        animation: true,
        label: {
          show: true
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
          opacity: 0.2
        }
      }
    },
    series: [{
      type: 'themeRiver',
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.8)'
        }
      },
      data: themeRiverData
    }]
  }

  themeRiverChart.setOption(option, true)
}

function renderHeatmap(data) {
  if (!heatmapChart || !data || data.length === 0) return

  const hours = Array.from({ length: 24 }, (_, i) => i + '点')
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  const maxValue = Math.max(...data.map(item => item[2]))

  const option = {
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return `${days[params.value[1]]} ${hours[params.value[0]]}<br />消费频次: ${params.value[2]}`
      }
    },
    grid: {
      height: '50%',
      top: '10%',
      left: '15%'
    },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: {
        show: true
      },
      axisLabel: {
        interval: 2
      }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: maxValue,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#f0f9ff', '#bae6fd', '#0ea5e9', '#0284c7']
      }
    },
    series: [{
      name: 'Punch Card',
      type: 'heatmap',
      data: data,
      label: {
        show: false
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }

  heatmapChart.setOption(option, true)
}

function renderRadarChart(data) {
  if (!radarChart || !data.indicator || data.indicator.length === 0) return

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        let res = params.name + '<br/>'
        data.indicator.forEach((item, index) => {
          res += item.name + ': ¥' + formatMoney(params.value[index]) + '<br/>'
        })
        return res
      }
    },
    legend: {
      data: data.series.map(item => item.name),
      top: 10
    },
    radar: {
      indicator: data.indicator,
      radius: '65%'
    },
    series: [{
      name: '季度消费结构',
      type: 'radar',
      data: data.series
    }]
  }

  radarChart.setOption(option, true)
}

function renderQuadrantChart(data) {
  if (!quadrantChart || !data || data.length === 0) return

  const avgFreq = data.reduce((sum, item) => sum + (item.frequency || 0), 0) / data.length
  const avgAmount = data.reduce((sum, item) => sum + (item.avg_amount || 0), 0) / data.length

  const option = {
    tooltip: {
      formatter: (params) => {
        const item = params.data
        return `
          <div style="font-weight:bold;margin-bottom:5px;">${item.name}</div>
          分类：${item.category}<br/>
          频次：${item.frequency} 次<br/>
          均价：¥${formatMoney(item.avg_amount)}<br/>
          总额：¥${formatMoney(item.total_amount)}
        `
      }
    },
    grid: {
      left: '5%',
      right: '10%',
      bottom: '10%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      name: '消费频次 (次)',
      type: 'log',
      logBase: 2,
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    yAxis: {
      name: '单笔均价 (元)',
      type: 'log',
      logBase: 2,
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      type: 'scatter',
      data: data.map(item => ({
        ...item,
        value: [item.frequency, item.avg_amount],
        symbolSize: Math.max(10, Math.min(Math.log(item.total_amount || 1) * 5, 60)),
        itemStyle: {
          color: getCategoryColor(item.category),
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        }
      })),
      markLine: {
        silent: true,
        lineStyle: {
          color: '#999',
          type: 'solid',
          width: 1
        },
        data: [
          { xAxis: avgFreq, name: '平均频次' },
          { yAxis: avgAmount, name: '平均均价' }
        ]
      }
    }]
  }

  quadrantChart.setOption(option, true)
}

function renderChordChart(data) {
  if (!chordChart || !data.nodes || data.nodes.length === 0) return

  let maxValue = 0
  let minValue = Infinity
  data.links.forEach(link => {
    maxValue = Math.max(maxValue, link.value || 0)
    minValue = Math.min(minValue, link.value || 0)
  })

  const coloredNodes = data.nodes.map(node => ({
    ...node,
    itemStyle: {
      color: getCategoryColor(node.name)
    }
  }))

  const processedLinks = (data.links || []).map(link => {
    let width = 1
    if (maxValue > minValue) {
      width = 1 + ((link.value || 0) - minValue) / (maxValue - minValue) * 7
    }
    return {
      ...link,
      lineStyle: {
        width: width,
        color: getCategoryColor(link.target),
        curveness: 0.3,
        opacity: 0.7
      },
      emphasis: {
        lineStyle: {
          width: width + 3,
          opacity: 1
        }
      }
    }
  })

  const option = {
    tooltip: {
      formatter: (params) => {
        if (params.dataType === 'edge') {
          return params.data.source + ' -> ' + params.data.target + '<br/>消费金额: ¥' + formatMoney(params.data.value)
        } else {
          return params.name
        }
      }
    },
    series: [{
      type: 'graph',
      layout: 'circular',
      circular: {
        rotateLabel: true
      },
      data: coloredNodes,
      links: processedLinks,
      roam: false,
      zoom: 0.75,
      label: {
        show: true,
        position: 'right',
        formatter: '{b}'
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          opacity: 1
        }
      },
      blur: {
        itemStyle: {
          opacity: 0.1
        },
        lineStyle: {
          opacity: 0.1
        }
      }
    }]
  }

  chordChart.setOption(option, true)
}

function renderFunnelChart(data) {
  if (!funnelChart || !data || data.length === 0) return

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        return params.name + ': ¥' + formatMoney(params.value) + ' (' + params.percent + '%)'
      }
    },
    series: [{
      name: '消费漏斗',
      type: 'funnel',
      left: '10%',
      top: 60,
      bottom: 60,
      width: '80%',
      min: 0,
      max: data[0].value,
      minSize: '0%',
      maxSize: '100%',
      sort: 'descending',
      gap: 2,
      label: {
        show: true,
        position: 'inside',
        formatter: '{b}'
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 1
      },
      data: data
    }]
  }

  funnelChart.setOption(option, true)
}

function renderParetoChart(data) {
  if (!paretoChart || !data.categories || data.categories.length === 0) return

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    grid: {
      right: '10%',
      left: '5%',
      bottom: '10%'
    },
    legend: {
      data: ['消费金额', '累积占比']
    },
    xAxis: [{
      type: 'category',
      data: data.categories,
      axisPointer: {
        type: 'shadow'
      },
      axisLabel: {
        interval: 0,
        rotate: 0
      }
    }],
    yAxis: [{
      type: 'value',
      name: '金额'
    }, {
      type: 'value',
      name: '累积占比',
      min: 0,
      max: 100,
      interval: 20,
      axisLabel: {
        formatter: '{value} %'
      }
    }],
    series: [{
      name: '消费金额',
      type: 'bar',
      data: data.values,
      itemStyle: {
        color: (params) => getCategoryColor(params.name)
      }
    }, {
      name: '累积占比',
      type: 'line',
      yAxisIndex: 1,
      data: data.percentages,
      itemStyle: {
        color: '#5470c6'
      },
      markLine: {
        data: [{ yAxis: 80, name: '80%线' }],
        lineStyle: {
          color: '#ee6666',
          type: 'dashed'
        }
      }
    }]
  }

  paretoChart.setOption(option, true)
}

function renderWordCloud(data) {
  if (!wordCloudChart || !data || data.length === 0) return

  const option = {
    tooltip: {
      show: true,
      formatter: (params) => {
        return params.name + ': ¥' + formatMoney(params.value)
      }
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '90%',
      height: '90%',
      sizeRange: [12, 60],
      rotationRange: [0, 0],
      rotationStep: 0,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: () => {
          return 'rgb(' + [
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160)
          ].join(',') + ')'
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: data
    }]
  }

  wordCloudChart.setOption(option, true)
}

function renderBoxPlot(data) {
  if (!boxPlotChart || !data.data || data.data.length === 0) return

  const alignedCategories = ['', ...data.categories]
  const alignedBoxData = [[], ...data.box_data]

  const getSeriesConfig = (isDetailMode) => {
    const seriesData = data.data.map(item => {
      let offset = isDetailMode ? 0.35 : 0
      const jitterRange = isDetailMode ? 0.5 : 0.6
      const jitter = (Math.random() - 0.5) * jitterRange
      return {
        value: [item.c + 1 + offset + jitter, item.v],
        merchant: item.m,
        date: item.d,
        categoryName: data.categories[item.c]
      }
    })

    return {
      boxWidth: isDetailMode ? '20%' : '50%',
      scatterData: seriesData
    }
  }

  const initialConfig = getSeriesConfig(false)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.seriesType === 'boxplot') {
          return `${params.name}<br/>
                  最大值: ${formatMoney(params.data[5])}<br/>
                  Q3: ${formatMoney(params.data[4])}<br/>
                  中位数: ${formatMoney(params.data[3])}<br/>
                  Q1: ${formatMoney(params.data[2])}<br/>
                  最小值: ${formatMoney(params.data[1])}`
        } else {
          const d = params.data
          return `<strong>${d.categoryName}</strong><br/>
                  ${d.date}<br/>
                  ${d.merchant}<br/>
                  <strong>¥${formatMoney(d.value[1])}</strong>`
        }
      }
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    },
    xAxis: [{
      type: 'category',
      data: alignedCategories,
      boundaryGap: true,
      axisLabel: {
        interval: 0,
        rotate: 0,
        formatter: (value) => {
          return value.length > 4 ? value.substring(0, 4) + '..' : value
        }
      }
    }, {
      type: 'value',
      min: -0.5,
      max: alignedCategories.length - 0.5,
      show: false
    }],
    yAxis: {
      type: 'log',
      logBase: 10,
      min: 1,
      name: '金额 (元)',
      splitLine: {
        show: true,
        lineStyle: {
          color: '#eee'
        }
      }
    },
    series: [{
      name: 'summary',
      type: 'boxplot',
      xAxisIndex: 0,
      data: alignedBoxData,
      boxWidth: initialConfig.boxWidth,
      itemStyle: {
        color: 'rgba(0, 0, 0, 0.02)',
        borderColor: '#666',
        borderWidth: 1.5
      },
      symbolSize: 0
    }, {
      name: 'transaction',
      type: 'scatter',
      xAxisIndex: 1,
      symbolSize: 6,
      itemStyle: {
        color: (params) => getCategoryColor(params.data.categoryName),
        opacity: 0.6
      },
      data: initialConfig.scatterData
    }]
  }

  boxPlotChart.setOption(option, true)
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

    await dataStore.loadAvailableYears()
    availableYears.value = dataStore.availableYears.sort((a, b) => b - a)

    if (availableYears.value.length > 0) {
      currentYear.value = availableYears.value[0]

      if (sessionStore.isDemo) {
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      await loadData(currentYear.value)
    }
  } catch (error) {
    console.error('Insights page init error:', error)
    uiStore.showError('页面初始化失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  scenarioChart?.dispose()
  themeRiverChart?.dispose()
  heatmapChart?.dispose()
  radarChart?.dispose()
  quadrantChart?.dispose()
  chordChart?.dispose()
  funnelChart?.dispose()
  paretoChart?.dispose()
  wordCloudChart?.dispose()
  boxPlotChart?.dispose()
  sankeyChart?.dispose()
})
</script>

<style scoped>
.insights-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
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

/* 顶部区域 */
.top-analysis-section {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  height: 500px;
}

.analysis-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-card);
}

.card-header {
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.card-content {
  min-height: 200px;
}

/* 桑基图卡片 */
.sankey-card {
  flex: 1;
  height: 100%;
  margin-bottom: 0 !important;
}

/* 年度故事卡片 */
.story-entry-card {
  width: 280px;
  flex-shrink: 0;
  height: 100%;
  margin-bottom: 0 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.story-entry-card:hover {
  transform: translateY(-2px);
}

.story-card-content {
  text-align: center;
}

.story-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.story-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.story-desc {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 20px;
}

.story-btn {
  padding: 8px 24px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 20px;
  font-size: 14px;
}

/* 核心分析网格 */
.core-analysis-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

/* 消费画像 */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  padding: 6px 12px;
  background: var(--hover-bg);
  color: var(--text-color);
  border-radius: 16px;
  font-size: 13px;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-feature {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
}

.feature-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 122, 255, 0.1);
  border-radius: 50%;
  color: #007AFF;
}

.feature-title {
  font-size: 12px;
  color: var(--secondary-text);
  margin-bottom: 2px;
}

.feature-description {
  font-size: 14px;
  color: var(--text-color);
  font-weight: 500;
}

/* 商家列表 */
.merchant-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.merchant-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
}

.merchant-item.top-1 .merchant-rank {
  background: linear-gradient(135deg, #FFD700, #FFA500);
}

.merchant-item.top-2 .merchant-rank {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
}

.merchant-item.top-3 .merchant-rank {
  background: linear-gradient(135deg, #CD7F32, #B87333);
}

.merchant-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.merchant-rank {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  font-weight: 600;
  font-size: 13px;
}

.merchant-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.merchant-meta {
  font-size: 12px;
  color: var(--secondary-text);
}

.merchant-stats {
  display: flex;
  gap: 16px;
}

.stat-group {
  text-align: right;
}

.stat-group .label {
  font-size: 11px;
  color: var(--secondary-text);
}

.stat-group .value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
}

/* 消费场景 */
.scenario-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  background: var(--bg-color);
  color: var(--secondary-text);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background: var(--hover-bg);
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.chart-container {
  height: 300px;
}

/* 消费习惯 */
.habit-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--secondary-text);
}

/* 高级洞察网格 */
.advanced-insights-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.insight-card {
  min-height: 180px;
}

.insight-stat-big {
  font-size: 32px;
  font-weight: 600;
  color: var(--text-color);
  text-align: center;
  margin-bottom: 8px;
}

.highlight {
  color: var(--primary-color);
  font-weight: 600;
}

.insight-desc {
  font-size: 13px;
  color: var(--secondary-text);
  text-align: center;
  margin-bottom: 4px;
}

.insight-meta {
  font-size: 12px;
  color: var(--text-color);
  text-align: center;
  opacity: 0.7;
}

.insight-list {
  margin-top: 12px;
}

.insight-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 12px;
  border-bottom: 1px solid var(--border-color);
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: var(--secondary-text);
  font-size: 13px;
}

/* 忠诚度 */
.loyalty-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loyalty-item {
  text-align: center;
}

.loyalty-value {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 4px;
}

.loyalty-details {
  display: flex;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
}

.loyalty-amount {
  color: var(--text-color);
}

.loyalty-tag {
  padding: 2px 8px;
  background: var(--primary-color);
  color: white;
  border-radius: 10px;
}

/* 高级可视化区域 */
.advanced-viz-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 20px 0;
}

.viz-section-header {
  margin: 30px 0 16px 0;
}

.section-subtitle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--secondary-text);
}

.full-width-viz-card {
  grid-column: 1 / -1;
}

.viz-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* 故事 Modal */
.story-modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 9999;
  justify-content: center;
  align-items: center;
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
}

.story-content {
  width: 100%;
  max-width: 420px;
  height: 75vh;
  min-height: 500px;
  position: relative;
  color: #333;
  display: flex;
  flex-direction: column;
}

.close-story {
  position: absolute;
  top: -50px;
  right: 0;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
}

.close-story:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: rotate(90deg);
}

.story-slides {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--radius-xl);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 1);
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease, transform 0.5s ease;
  transform: scale(0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px;
  pointer-events: none;
}

.slide.active {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

.slide-number {
  font-size: 48px;
  font-weight: 600;
  color: var(--border-color);
  margin-bottom: 20px;
}

.slide-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 16px;
}

.slide-content {
  font-size: 18px;
  color: var(--secondary-text);
  line-height: 1.6;
  max-width: 600px;
}

.slide-content h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #1d1d1f;
  font-weight: 800;
}

.slide-content h2 {
  font-size: 24px;
  margin-bottom: 30px;
  color: #1d1d1f;
  font-weight: 700;
}

.slide-content p {
  margin-bottom: 12px;
  color: var(--secondary-text);
}

.slide-date {
  font-size: 18px;
  color: #86868b;
  margin-bottom: 10px;
  font-weight: 500;
}

.slide-amount {
  font-size: 40px;
  font-weight: 800;
  background: linear-gradient(135deg, #FF9500 0%, #FF3B30 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 20px;
  font-family: var(--font-family-mono);
}

.slide-keyword {
  font-size: 36px;
  font-weight: 800;
  color: #007AFF;
  margin-bottom: 20px;
}

.slide-big-icon {
  font-size: 80px;
  color: rgba(0, 0, 0, 0.05);
  margin-top: 40px;
}

.story-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

/* 翻页按钮样式 - 使用更具体的选择器避免覆盖卡片中的按钮 */
.story-controls .story-btn {
  background: none;
  border: none;
  color: white !important;
  font-size: 24px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.story-controls .story-btn:hover {
  opacity: 1;
}

.story-indicators {
  display: flex;
  gap: 8px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
}

.indicator.active {
  background: white;
  transform: scale(1.2);
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

@media (max-width: 1200px) {
  .top-analysis-section {
    flex-direction: column;
    height: auto;
  }

  .sankey-card {
    height: 400px;
  }

  .story-entry-card {
    width: 100%;
    height: 200px;
  }

  .core-analysis-grid {
    grid-template-columns: 1fr;
  }

  .advanced-insights-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .viz-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    grid-template-columns: 1fr;
    gap: 16px;
    text-align: center;
  }

  .habit-stats {
    grid-template-columns: 1fr;
  }
}
</style>
