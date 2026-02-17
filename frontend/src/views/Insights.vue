<template>
  <div class="insights-page">
    <div class="page-header">
      <h1 class="page-title">消费洞察</h1>
      <div class="header-actions">
        <select v-model="filters.year" @change="loadData" class="filter-select">
          <option value="">选择年份</option>
          <option v-for="year in dataStore.availableYears" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
      </div>
    </div>

    <div v-if="uiStore.globalLoading && !insightsData" class="page-loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="insightsData" class="insights-content">
      <!-- 消费习惯 -->
      <section class="insight-section">
        <h2 class="section-title">
          <i class="fas fa-chart-line"></i>
          消费习惯
        </h2>
        <div class="habits-grid">
          <div class="habit-card">
            <div class="habit-icon" style="background: rgba(0, 122, 255, 0.1)">
              <i class="fas fa-calendar-day" style="color: #007AFF"></i>
            </div>
            <div class="habit-content">
              <p class="habit-label">最常消费日</p>
              <p class="habit-value">{{ insightsData.habits?.most_common_day || '-' }}</p>
            </div>
          </div>
          <div class="habit-card">
            <div class="habit-icon" style="background: rgba(255, 149, 0, 0.1)">
              <i class="fas fa-clock" style="color: #FF9500"></i>
            </div>
            <div class="habit-content">
              <p class="habit-label">最常消费时段</p>
              <p class="habit-value">{{ insightsData.habits?.most_common_hour || '-' }}</p>
            </div>
          </div>
          <div class="habit-card">
            <div class="habit-icon" style="background: rgba(52, 199, 89, 0.1)">
              <i class="fas fa-redo" style="color: #34C759"></i>
            </div>
            <div class="habit-content">
              <p class="habit-label">消费频率</p>
              <p class="habit-value">{{ insightsData.habits?.frequency || '-' }}</p>
            </div>
          </div>
          <div class="habit-card">
            <div class="habit-icon" style="background: rgba(175, 82, 222, 0.1)">
              <i class="fas fa-coffee" style="color: #AF52DE"></i>
            </div>
            <div class="habit-content">
              <p class="habit-label">小额消费占比</p>
              <p class="habit-value">{{ insightsData.habits?.small_expense_ratio || '-' }}%</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 热门商户 -->
      <section class="insight-section">
        <h2 class="section-title">
          <i class="fas fa-store"></i>
          热门商户
        </h2>
        <div class="merchants-list">
          <div
            v-for="(merchant, index) in topMerchants"
            :key="merchant.name"
            class="merchant-item"
          >
            <div class="merchant-rank" :style="{ background: getRankColor(index) }">
              {{ index + 1 }}
            </div>
            <div class="merchant-info">
              <p class="merchant-name">{{ merchant.name }}</p>
              <p class="merchant-count">{{ merchant.count }} 笔</p>
            </div>
            <div class="merchant-amount">
              ¥{{ formatMoney(merchant.amount) }}
            </div>
          </div>
        </div>
      </section>

      <!-- 消费场景 -->
      <section class="insight-section">
        <h2 class="section-title">
          <i class="fas fa-map-marker-alt"></i>
          消费场景
        </h2>
        <div class="scenarios-grid">
          <div
            v-for="scenario in scenarios"
            :key="scenario.name"
            class="scenario-card"
          >
            <div class="scenario-icon" :style="{ background: scenario.color + '20' }">
              <i :class="scenario.icon" :style="{ color: scenario.color }"></i>
            </div>
            <p class="scenario-name">{{ scenario.name }}</p>
            <p class="scenario-amount">¥{{ formatMoney(scenario.amount) }}</p>
            <p class="scenario-count">{{ scenario.count }} 笔</p>
          </div>
        </div>
      </section>

      <!-- 账单画像 -->
      <section class="insight-section">
        <h2 class="section-title">
          <i class="fas fa-user-circle"></i>
          账单画像
        </h2>
        <div class="profile-container">
          <div class="profile-tag" v-for="tag in profileTags" :key="tag">
            {{ tag }}
          </div>
        </div>
      </section>

      <!-- 建议 -->
      <section class="insight-section">
        <h2 class="section-title">
          <i class="fas fa-lightbulb"></i>
          个性化建议
        </h2>
        <div class="suggestions-list">
          <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-item">
            <i class="fas fa-check-circle suggestion-icon"></i>
            <p>{{ suggestion }}</p>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="empty-state">
      <i class="fas fa-lightbulb empty-icon"></i>
      <p>请选择年份查看消费洞察</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDataStore } from '@/stores/data'
import { useUiStore } from '@/stores/ui'
import { formatMoney } from '@/utils/format'

const dataStore = useDataStore()
const uiStore = useUiStore()

const filters = ref({
  year: null
})

const insightsData = ref(null)

const topMerchants = computed(() => {
  return insightsData.value?.top_merchants || []
})

const scenarios = computed(() => {
  const rawScenarios = insightsData.value?.scenarios || []
  return rawScenarios.map(s => {
    const iconMap = {
      '餐饮': 'fas fa-utensils',
      '购物': 'fas fa-shopping-bag',
      '交通': 'fas fa-car',
      '娱乐': 'fas fa-gamepad',
      '医疗': 'fas fa-hospital',
      '教育': 'fas fa-graduation-cap'
    }
    const colorMap = {
      '餐饮': '#FF3B30',
      '购物': '#FF9500',
      '交通': '#007AFF',
      '娱乐': '#AF52DE',
      '医疗': '#34C759',
      '教育': '#5856D6'
    }
    return {
      ...s,
      icon: iconMap[s.type] || 'fas fa-tag',
      color: colorMap[s.type] || '#8E8E93'
    }
  })
})

const profileTags = computed(() => {
  return insightsData.value?.profile_tags || []
})

const suggestions = computed(() => {
  return insightsData.value?.suggestions || []
})

function getRankColor(index) {
  const colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#007AFF', '#8E8E93']
  return colors[index] || colors[4]
}

async function loadData() {
  if (!filters.value.year) {
    insightsData.value = null
    return
  }

  try {
    uiStore.setGlobalLoading(true)
    insightsData.value = await dataStore.loadAnalysisData({
      year: filters.value.year
    })
  } catch (error) {
    uiStore.showError('加载数据失败: ' + error.message)
  } finally {
    uiStore.setGlobalLoading(false)
  }
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
</script>

<style scoped>
.insights-page {
  max-width: 1200px;
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

.insight-section {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 20px 0;
}

.section-title i {
  color: var(--primary-color);
}

.habits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.habit-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
}

.habit-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
}

.habit-icon i {
  font-size: 20px;
}

.habit-content {
  flex: 1;
}

.habit-label {
  font-size: 13px;
  color: var(--secondary-text);
  margin: 0 0 4px 0;
}

.habit-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.merchants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.merchant-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
}

.merchant-rank {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.merchant-info {
  flex: 1;
}

.merchant-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-color);
  margin: 0 0 2px 0;
}

.merchant-count {
  font-size: 13px;
  color: var(--secondary-text);
  margin: 0;
}

.merchant-amount {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.scenario-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
  text-align: center;
}

.scenario-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 12px;
}

.scenario-icon i {
  font-size: 24px;
}

.scenario-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  margin: 0 0 8px 0;
}

.scenario-amount {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 4px 0;
}

.scenario-count {
  font-size: 12px;
  color: var(--secondary-text);
  margin: 0;
}

.profile-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.profile-tag {
  padding: 8px 16px;
  background: var(--bg-color);
  color: var(--text-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--primary-color);
}

.suggestion-icon {
  color: var(--success-color);
  font-size: 18px;
  margin-top: 2px;
  flex-shrink: 0;
}

.suggestion-item p {
  margin: 0;
  font-size: 14px;
  color: var(--text-color);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .habits-grid,
  .scenarios-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
