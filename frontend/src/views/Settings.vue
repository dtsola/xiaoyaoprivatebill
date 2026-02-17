<template>
  <div class="settings-page">
    <div class="page-header">
      <h1 class="page-title">设置</h1>
    </div>

    <!-- 文件上传区域 -->
    <section class="settings-section">
      <h2 class="section-title">上传账单</h2>
      <p class="section-desc">支持支付宝 CSV 格式和微信 CSV/XLSX 格式账单</p>

      <div
        class="upload-area"
        :class="{ dragging: isDragging, uploading: isUploading }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept=".csv,.xlsx"
          multiple
          style="display: none"
          @change="handleFileSelect"
        />
        <i class="fas fa-cloud-upload-alt upload-icon"></i>
        <p class="upload-text">点击或拖拽文件到此处上传</p>
        <p class="upload-hint">支持 CSV、XLSX 格式，最大 16MB</p>
      </div>
    </section>

    <!-- 已上传文件列表 -->
    <section class="settings-section">
      <h2 class="section-title">已上传文件</h2>

      <div v-if="sessionStore.uploadedFiles.length === 0" class="empty-state">
        <i class="fas fa-file-alt empty-icon"></i>
        <p>暂无上传文件</p>
      </div>

      <div v-else class="file-list">
        <div v-for="file in sessionStore.uploadedFiles" :key="file" class="file-item">
          <i class="fas fa-file-alt file-icon"></i>
          <span class="file-name">{{ file }}</span>
          <button class="file-delete" @click="handleDeleteFile(file)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- 数据管理 -->
    <section class="settings-section">
      <h2 class="section-title">数据管理</h2>

      <div class="action-buttons">
        <button class="btn btn-danger" @click="handleClearData">
          <i class="fas fa-trash-alt"></i>
          清除所有数据
        </button>
      </div>
    </section>

    <!-- 演示模式 -->
    <section class="settings-section" v-if="!sessionStore.isDemo">
      <h2 class="section-title">演示模式</h2>
      <p class="section-desc">体验系统功能，无需上传真实数据</p>

      <button class="btn btn-primary" @click="handleEnterDemo">
        <i class="fas fa-play"></i>
        进入演示模式
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSessionStore } from '@/stores/session'
import { useUiStore } from '@/stores/ui'

const sessionStore = useSessionStore()
const uiStore = useUiStore()

const fileInput = ref(null)
const isDragging = ref(false)
const isUploading = ref(false)

onMounted(() => {
  loadFiles()
})

async function loadFiles() {
  try {
    await sessionStore.loadUploadedFiles()
  } catch (error) {
    uiStore.showError('加载文件列表失败: ' + error.message)
  }
}

function triggerFileInput() {
  fileInput.value?.click()
}

async function handleFileSelect(event) {
  const files = event.target.files
  if (files.length > 0) {
    await uploadFiles(Array.from(files))
  }
  // 重置 input 以允许再次选择同一文件
  event.target.value = ''
}

async function handleDrop(event) {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files).filter(file =>
    file.name.endsWith('.csv') || file.name.endsWith('.xlsx')
  )
  if (files.length > 0) {
    await uploadFiles(files)
  }
}

async function uploadFiles(files) {
  isUploading.value = true
  try {
    for (const file of files) {
      await sessionStore.uploadFile(file)
    }
    uiStore.showSuccess(`成功上传 ${files.length} 个文件`)
    await loadFiles()
  } catch (error) {
    uiStore.showError('上传失败: ' + error.message)
  } finally {
    isUploading.value = false
  }
}

async function handleDeleteFile(filename) {
  if (confirm(`确定要删除文件 "${filename}" 吗？`)) {
    try {
      await sessionStore.deleteFile(filename)
      uiStore.showSuccess('文件已删除')
      await loadFiles()
    } catch (error) {
      uiStore.showError('删除失败: ' + error.message)
    }
  }
}

async function handleClearData() {
  if (confirm('确定要清除所有数据吗？此操作不可恢复！')) {
    try {
      await sessionStore.clearAllData()
      uiStore.showSuccess('数据已清除')
    } catch (error) {
      uiStore.showError('清除失败: ' + error.message)
    }
  }
}

async function handleEnterDemo() {
  try {
    await sessionStore.enterDemoMode()
    uiStore.showSuccess('已进入演示模式')
    // 跳转到首页
    window.location.href = '/'
  } catch (error) {
    uiStore.showError('进入演示模式失败: ' + error.message)
  }
}
</script>

<style scoped>
.settings-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-color);
}

.settings-section {
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 8px 0;
}

.section-desc {
  color: var(--secondary-text);
  font-size: 14px;
  margin: 0 0 16px 0;
}

.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-lg);
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover,
.upload-area.dragging {
  border-color: var(--primary-color);
  background: var(--hover-bg);
}

.upload-area.uploading {
  pointer-events: none;
  opacity: 0.6;
}

.upload-icon {
  font-size: 48px;
  color: var(--secondary-text);
  margin-bottom: 16px;
}

.upload-text {
  font-size: 16px;
  color: var(--text-color);
  margin: 0 0 8px 0;
}

.upload-hint {
  font-size: 13px;
  color: var(--secondary-text);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--secondary-text);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
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
}

.file-icon {
  color: var(--primary-color);
  font-size: 18px;
}

.file-name {
  flex: 1;
  font-size: 14px;
  color: var(--text-color);
}

.file-delete {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--secondary-text);
  border-radius: var(--radius-sm);
}

.file-delete:hover {
  color: var(--danger-color);
  background: rgba(255, 59, 48, 0.1);
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
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

.btn-danger {
  background: var(--danger-color);
  color: white;
}

.btn-danger:hover {
  background: #E6352A;
}
</style>
