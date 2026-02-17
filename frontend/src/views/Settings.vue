<template>
  <div class="settings-page">
    <!-- 页面标题和会话计时器 -->
    <div class="page-header">
      <h1 class="page-title">文件管理</h1>
      <div class="session-timer">
        <i class="fas fa-clock"></i>
        <span>会话剩余时间: <span id="timeRemaining">{{ timeRemaining }}</span></span>
      </div>
    </div>

    <!-- 双栏布局：支付宝和微信 -->
    <div class="split-layout">
      <!-- 左侧：支付宝专区 -->
      <div class="provider-column alipay-column">
        <h2 class="column-header">
          <i class="fab fa-alipay"></i> 支付宝账单
        </h2>

        <!-- 支付宝指南 -->
        <div class="upload-guide">
          <h3>如何获取支付宝账单？</h3>
          <ol>
            <li>打开支付宝 App -> 我的 -> 账单</li>
            <li>右上角 ... -> 开具交易流水证明 -> 用于个人对账 -> 申请</li>
            <li>自定义时间范围（最长为一年） -> 填写邮箱 -> 下载账单</li>
            <li>申请记录中找到解压密码 -> 解压下载的文件，获取 CSV 文件</li>
            <li>按年份重命名为【alipay_record_2026.csv】格式</li>
          </ol>
        </div>

        <!-- 支付宝上传区域 -->
        <label
          class="file-upload"
          :class="{ dragover: alipayDragging }"
          @dragover.prevent="alipayDragging = true"
          @dragleave.prevent="alipayDragging = false"
          @drop.prevent="handleAlipayDrop"
        >
          <input
            ref="alipayInput"
            type="file"
            accept=".csv"
            multiple
            @change="handleAlipayFileSelect"
          />
          <div class="upload-icon">
            <i class="fas fa-file-csv"></i>
          </div>
          <div class="upload-text">
            点击或拖拽<br />支付宝 CSV 文件
            <br /><span style="font-size: 12px; opacity: 0.7;">最大 16MB</span>
          </div>
        </label>

        <!-- 支付宝文件列表 -->
        <div class="file-list-container">
          <h4>已上传文件</h4>
          <div class="file-list">
            <div v-for="file in alipayFiles" :key="file.name" class="file-item">
              <i :class="file.name.endsWith('.xlsx') ? 'fas fa-file-excel' : 'fas fa-file-csv'"></i>
              <span class="file-name">{{ file.name }}</span>
              <div class="file-actions">
                <span class="file-status status-success">已上传</span>
                <button class="delete-btn" @click="deleteFile(file.name)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：微信专区 -->
      <div class="provider-column wechat-column">
        <h2 class="column-header">
          <i class="fab fa-weixin"></i> 微信账单
        </h2>

        <!-- 微信指南 -->
        <div class="upload-guide">
          <h3>如何获取微信账单？</h3>
          <ol>
            <li>打开微信 App -> 我 -> 服务 -> 钱包 -> 账单</li>
            <li>点击右上角 [...] -> 账单下载 -> 用于个人对账</li>
            <li>选择接收方式（微信/邮箱）、账单时间 -> 下一步</li>
            <li><strong>方式一（推荐）：</strong>刷脸验证 -> 微信消息直接下载 XLSX 文件</li>
            <li><strong>方式二：</strong>输入邮箱 -> 刷脸 -> 邮箱接收 (密码在微信消息中)</li>
          </ol>
        </div>

        <!-- 微信上传区域 -->
        <label
          class="file-upload"
          :class="{ dragover: wechatDragging }"
          @dragover.prevent="wechatDragging = true"
          @dragleave.prevent="wechatDragging = false"
          @drop.prevent="handleWechatDrop"
        >
          <input
            ref="wechatInput"
            type="file"
            accept=".xlsx,.csv"
            multiple
            @change="handleWechatFileSelect"
          />
          <div class="upload-icon">
            <i class="fas fa-file-invoice"></i>
          </div>
          <div class="upload-text">
            点击或拖拽<br />微信 XLSX/CSV 文件
            <br /><span style="font-size: 12px; opacity: 0.7;">最大 16MB</span>
          </div>
        </label>

        <!-- 微信文件列表 -->
        <div class="file-list-container">
          <h4>已上传文件</h4>
          <div class="file-list">
            <div v-for="file in wechatFiles" :key="file.name" class="file-item">
              <i :class="file.name.endsWith('.xlsx') ? 'fas fa-file-excel' : 'fas fa-file-csv'"></i>
              <span class="file-name">{{ file.name }}</span>
              <div class="file-actions">
                <span class="file-status status-success">已上传</span>
                <button class="delete-btn" @click="deleteFile(file.name)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-action-bar" :class="{ visible: totalFileCount > 0 }">
      <div class="action-bar-content">
        <div class="file-summary">
          <i class="fas fa-file-alt"></i>
          <span>{{ totalFileCount > 0 ? `已就绪 ${totalFileCount} 个账单文件` : '请上传账单文件' }}</span>
        </div>
        <div class="action-buttons">
          <router-link to="/yearly" class="start-button" :class="{ disabled: totalFileCount === 0 }">
            <i class="fas fa-chart-line"></i>
            开始分析
          </router-link>
        </div>
      </div>
    </div>

    <!-- 删除区域 -->
    <div class="delete-section">
      <h2 class="section-title">数据管理</h2>
      <div class="delete-area">
        <button class="delete-all-btn" @click="handleClearAllData">
          <i class="fas fa-trash-alt"></i>
          删除所有账单数据
        </button>
        <p class="delete-warning">删除后将清空所有已上传的账单文件和分析数据，此操作不可恢复。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

const router = useRouter()
const sessionStore = useSessionStore()
const uiStore = useUiStore()

// 文件列表
const alipayFiles = ref([])
const wechatFiles = ref([])

// 拖拽状态
const alipayDragging = ref(false)
const wechatDragging = ref(false)

// 文件输入引用
const alipayInput = ref(null)
const wechatInput = ref(null)

// 会话计时器
const timeRemaining = ref('--:--')
let timerInterval = null

// 总文件数
const totalFileCount = computed(() => alipayFiles.value.length + wechatFiles.value.length)

// 最大文件大小 16MB
const MAX_FILE_SIZE = 16 * 1024 * 1024

onMounted(async () => {
  await loadFiles()
  startTimer()
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})

// 加载已上传文件
async function loadFiles() {
  try {
    const data = await api.getFiles()
    console.log('[Settings] Loaded files:', data)

    // 清空现有列表
    alipayFiles.value = []
    wechatFiles.value = []

    // 根据文件来源分类
    data.files.forEach(file => {
      // 使用后端返回的 source 字段判断，如果不存在则回退到扩展名判断
      let isWechat = false
      if (file.source) {
        isWechat = file.source === 'wechat'
      } else {
        isWechat = file.name.endsWith('.xlsx')
      }

      if (isWechat) {
        wechatFiles.value.push(file)
      } else {
        alipayFiles.value.push(file)
      }
    })

    // 排序文件列表
    sortFileList(alipayFiles)
    sortFileList(wechatFiles)
  } catch (error) {
    console.error('[Settings] 加载文件列表失败:', error)
  }
}

// 排序文件列表
function sortFileList(fileList) {
  fileList.sort((a, b) => {
    return a.name.localeCompare(b.name, 'zh-CN', { numeric: true })
  })
}

// 检查文件大小
function checkFileSize(file) {
  if (file.size > MAX_FILE_SIZE) {
    uiStore.showError(`文件 ${file.name} 超过大小限制（16MB）`)
    return false
  }
  return true
}

// 检查是否在演示模式
function checkDemoMode() {
  if (sessionStore.isDemo) {
    uiStore.showError('演示模式下无法上传文件，请先退出演示模式')
    return false
  }
  return true
}

// 处理支付宝文件选择
async function handleAlipayFileSelect(event) {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    await handleFiles(files, '.csv', 'alipay')
  }
  // 重置 input
  event.target.value = ''
}

// 处理微信文件选择
async function handleWechatFileSelect(event) {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    await handleFiles(files, '.xlsx,.csv', 'wechat')
  }
  // 重置 input
  event.target.value = ''
}

// 处理支付宝拖放
async function handleAlipayDrop(event) {
  alipayDragging.value = false
  const files = Array.from(event.dataTransfer.files).filter(file =>
    file.name.toLowerCase().endsWith('.csv')
  )
  if (files.length > 0) {
    await handleFiles(files, '.csv', 'alipay')
  }
}

// 处理微信拖放
async function handleWechatDrop(event) {
  wechatDragging.value = false
  const files = Array.from(event.dataTransfer.files).filter(file =>
    file.name.toLowerCase().endsWith('.xlsx') || file.name.toLowerCase().endsWith('.csv')
  )
  if (files.length > 0) {
    await handleFiles(files, '.xlsx,.csv', 'wechat')
  }
}

// 处理文件上传
async function handleFiles(files, allowedExt, provider) {
  if (!checkDemoMode()) return

  const allowedExtensions = allowedExt.split(',').map(e => e.trim().toLowerCase())

  for (const file of files) {
    const fileName = file.name.toLowerCase()
    const isAllowed = allowedExtensions.some(ext => fileName.endsWith(ext))

    if (!isAllowed) {
      uiStore.showError(`请上传 ${allowedExt} 格式的文件`)
      continue
    }

    if (!checkFileSize(file)) continue

    try {
      uiStore.setGlobalLoading(true)
      const formData = new FormData()
      formData.append('file', file)

      const result = await api.uploadFile(formData)

      // 添加到对应的文件列表
      const newFile = { name: result.filename || file.name, source: provider }
      if (provider === 'wechat') {
        wechatFiles.value.push(newFile)
        sortFileList(wechatFiles)
      } else {
        alipayFiles.value.push(newFile)
        sortFileList(alipayFiles)
      }

      uiStore.showSuccess('文件上传成功')
    } catch (error) {
      uiStore.showError('上传失败: ' + error.message)
    } finally {
      uiStore.setGlobalLoading(false)
    }
  }
}

// 删除文件
async function deleteFile(filename) {
  if (confirm(`确定要删除文件 "${filename}" 吗？`)) {
    try {
      await api.deleteFile(filename)

      // 从列表中移除
      alipayFiles.value = alipayFiles.value.filter(f => f.name !== filename)
      wechatFiles.value = wechatFiles.value.filter(f => f.name !== filename)

      uiStore.showSuccess('文件已删除')
    } catch (error) {
      uiStore.showError('删除失败: ' + error.message)
    }
  }
}

// 清除所有数据
async function handleClearAllData() {
  if (confirm('确定要删除所有账单数据吗？此操作不可恢复！')) {
    try {
      await api.clearData()

      // 清空文件列表
      alipayFiles.value = []
      wechatFiles.value = []

      // 重置计时器
      timeRemaining.value = '--:--'

      uiStore.showSuccess('所有数据已清除')
    } catch (error) {
      uiStore.showError('清除失败: ' + error.message)
    }
  }
}

// 开始计时器
function startTimer() {
  updateTimer()
  timerInterval = setInterval(updateTimer, 1000)
}

// 更新计时器
async function updateTimer() {
  try {
    const data = await api.getTimeRemaining()

    // 如果会话还未开始（没有上传文件）
    if (!data.hasOwnProperty('remaining')) {
      timeRemaining.value = '--:--'
      return
    }

    const remaining = data.remaining
    if (remaining <= 0 || data.expired) {
      timeRemaining.value = '已过期'
      // 如果有文件则重定向到首页
      if (totalFileCount.value > 0) {
        router.push('/')
      }
      return
    }

    const minutes = Math.floor(remaining / 60)
    const seconds = remaining % 60
    timeRemaining.value = `${minutes}:${seconds.toString().padStart(2, '0')}`
  } catch (error) {
    console.error('[Settings] 更新计时器失败:', error)
  }
}
</script>

<style scoped>
/* 基础样式 */
.settings-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px 140px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.session-timer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  color: var(--secondary-text);
  font-size: 14px;
}

.session-timer i {
  color: var(--primary-color);
}

/* 双栏布局 */
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.provider-column {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.provider-column:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.column-header {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.column-header i {
  font-size: 20px;
}

.alipay-column .column-header i {
  color: #00A0E9;
}

.wechat-column .column-header i {
  color: #07C160;
}

/* 上传指南 */
.upload-guide {
  background: #fbfbfd;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 24px;
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.upload-guide h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
  margin-top: 0;
}

.upload-guide ol {
  margin: 0;
  padding-left: 20px;
}

.upload-guide li {
  font-size: 13px;
  line-height: 1.6;
  color: #424245;
  margin-bottom: 8px;
}

.upload-guide li strong {
  color: #1d1d1f;
  font-weight: 600;
}

/* 文件上传区域 */
.file-upload {
  display: block;
  border: 2px dashed #d2d2d7;
  background: #fafafc;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 180px;
}

.file-upload:hover,
.file-upload.dragover {
  border-color: #007aff;
  background: #f0f8ff;
  transform: scale(1.02);
}

.file-upload input[type="file"] {
  display: none;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-icon i {
  color: #86868b;
  transition: color 0.2s ease;
}

.file-upload:hover .upload-icon i {
  color: #007aff;
  transform: scale(1.1);
}

.upload-text {
  color: #86868b;
  font-size: 14px;
  font-weight: 500;
}

/* 文件列表 */
.file-list-container {
  margin-top: 24px;
}

.file-list-container h4 {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  margin: 0 0 12px 0;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-color);
  border-radius: var(--radius-sm);
  transition: background-color 0.2s;
}

.file-item:hover {
  background: var(--hover-bg);
}

.file-item > i {
  color: var(--primary-color);
  font-size: 18px;
}

.file-name {
  flex: 1;
  font-size: 13px;
  color: var(--text-color);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-status {
  font-size: 12px;
  color: var(--secondary-text);
}

.file-status.status-success {
  color: #34C759;
}

.delete-btn {
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
  color: var(--secondary-text);
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}

.delete-btn:hover {
  color: var(--danger-color);
  background: rgba(255, 59, 48, 0.1);
}

/* 底部操作栏 */
.bottom-action-bar {
  position: fixed;
  bottom: 0;
  left: var(--sidebar-width);
  right: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: saturate(180%) blur(20px);
  border-top: 1px solid var(--border-color);
  padding: 16px 20px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  z-index: 1000;
}

.bottom-action-bar.visible {
  transform: translateY(0);
}

.action-bar-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-summary {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--text-color);
}

.file-summary i {
  color: var(--primary-color);
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
}

.start-button:hover:not(.disabled) {
  background: #0066E6;
  transform: translateY(-1px);
}

.start-button.disabled {
  opacity: 0.3;
  cursor: not-allowed;
  pointer-events: none;
}

/* 删除区域 */
.delete-section {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-top: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 16px 0;
}

.delete-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.delete-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--danger-color);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-all-btn:hover {
  background: #E6352A;
}

.delete-warning {
  font-size: 13px;
  color: var(--secondary-text);
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .split-layout {
    grid-template-columns: 1fr;
  }

  .bottom-action-bar {
    left: 0;
    padding: 12px 16px;
  }

  .action-bar-content {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .start-button {
    justify-content: center;
  }

  .settings-page {
    padding: 0 16px 140px 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .session-timer {
    align-self: flex-start;
  }
}
</style>
