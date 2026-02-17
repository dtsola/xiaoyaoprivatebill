<template>
  <div class="welcome-section">
    <h1 class="welcome-title">全能账单分析工具</h1>
    <p class="welcome-subtitle">
      支持支付宝和微信账单的一站式分析，获取详细的消费洞察。<br />
      所有数据分析均在本地进行，保护您的隐私安全。
    </p>

    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon feature-icon-analysis">
          <i class="fas fa-chart-pie"></i>
        </div>
        <h3 class="feature-title">多维度分析</h3>
        <p class="feature-description">
          支持年度、月度、分类、时间等多个维度的消费分析，帮助您更好地了解消费习惯。
        </p>
      </div>
      <div class="feature-card">
        <div class="feature-icon feature-icon-privacy">
          <i class="fas fa-shield-alt"></i>
        </div>
        <h3 class="feature-title">隐私保护</h3>
        <p class="feature-description">
          数据仅在浏览器中分析，不会永久存储。会话结束后自动删除所有上传的文件。
        </p>
      </div>
      <div class="feature-card">
        <div class="feature-icon feature-icon-trend">
          <i class="fas fa-chart-line"></i>
        </div>
        <h3 class="feature-title">趋势追踪</h3>
        <p class="feature-description">
          展示消费趋势变化，支持环比分析，帮助您更好地规划财务。
        </p>
      </div>
      <div class="feature-card">
        <div class="feature-icon feature-icon-search">
          <i class="fas fa-search"></i>
        </div>
        <h3 class="feature-title">智能搜索</h3>
        <p class="feature-description">
          支持交易记录快速搜索和筛选，轻松找到任意历史交易信息。
        </p>
      </div>
    </div>

    <div class="upload-section">
      <h2 class="upload-title">开始分析您的账单</h2>
      <p class="privacy-notice">
        支持导入支付宝(CSV)和微信(XLSX)账单文件，文件将在会话结束后自动删除。<br />
        所有数据分析均在本地进行，我们不会收集或存储您的个人信息。
      </p>
      <div class="action-buttons">
        <router-link to="/settings" class="start-button">
          <i class="fas fa-upload"></i>
          上传账单文件
        </router-link>
        <button @click="enterDemoMode" class="demo-button">
          <i class="fas fa-eye"></i>
          查看示例数据
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const uiStore = useUiStore()
const sessionStore = useSessionStore()

async function enterDemoMode() {
  try {
    await sessionStore.enterDemoMode()
    uiStore.showSuccess('已进入演示模式')
    router.push('/yearly')
  } catch (error) {
    console.error('Error:', error)
    uiStore.showError('进入演示模式失败: ' + error.message)
  }
}
</script>

<style scoped>
/* 完全复制老前端的样式 */
.welcome-section {
  text-align: center;
  padding: 48px 24px;
  max-width: 800px;
  margin: 0 auto;
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 16px;
  letter-spacing: -0.025em;
}

.welcome-subtitle {
  font-size: 18px;
  color: var(--secondary-text);
  margin-bottom: 48px;
  line-height: 1.5;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.feature-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: left;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.feature-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  font-size: 24px;
}

/* 为每个特色图标添加彩色背景 */
.feature-icon-analysis {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
}

.feature-icon-privacy {
  background: rgba(52, 199, 89, 0.1);
  color: #34C759;
}

.feature-icon-trend {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
}

.feature-icon-search {
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
}

.feature-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 12px;
}

.feature-description {
  font-size: 14px;
  color: var(--secondary-text);
  line-height: 1.5;
  margin: 0;
}

.upload-section {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 48px;
  text-align: center;
}

.upload-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 16px;
}

.privacy-notice {
  font-size: 14px;
  color: var(--secondary-text);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
  min-width: 180px;
  height: 48px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.start-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.start-button i {
  font-size: 18px;
}

.demo-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: var(--primary-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 180px;
  height: 48px;
  justify-content: center;
}

.demo-button:hover {
  background: var(--hover-bg);
  transform: translateY(-1px);
  box-shadow: var(--shadow-card);
}

@media (max-width: 768px) {
  .start-button {
    padding: 10px 20px;
    font-size: 14px;
    min-width: 120px;
  }
}
</style>
