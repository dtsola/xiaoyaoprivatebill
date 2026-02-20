import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import api from '@/api/client'

// LocalStorage key
const DEMO_MODE_KEY = 'xiaoyao_demo_mode'

export const useSessionStore = defineStore('session', () => {
  // 从 localStorage 恢复演示模式状态
  const savedDemoMode = localStorage.getItem(DEMO_MODE_KEY) === 'true'

  // 状态
  const isDemo = ref(savedDemoMode)
  const uploadedFiles = ref([])
  const isLoading = ref(false)
  const sessionActive = ref(false)

  // 监听 isDemo 变化，同步到 localStorage
  watch(isDemo, (newValue) => {
    localStorage.setItem(DEMO_MODE_KEY, String(newValue))
    console.log('[Session] Demo mode saved to localStorage:', newValue)
  })

  // 计算属性
  const hasData = computed(() => uploadedFiles.value.length > 0)

  // ==================== 演示模式 ====================

  /**
   * 进入演示模式
   */
  async function enterDemoMode() {
    try {
      console.log('[Session] Entering demo mode...')
      isLoading.value = true
      const result = await api.enterDemo()
      console.log('[Session] Demo mode API result:', result)

      // 直接设置本地状态
      isDemo.value = true
      sessionActive.value = true

      console.log('[Session] Demo mode entered successfully, isDemo:', isDemo.value)
    } catch (error) {
      console.error('[Session] 进入演示模式失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 退出演示模式
   */
  async function exitDemoMode() {
    try {
      isLoading.value = true
      await api.exitDemo()

      // 清除本地状态
      isDemo.value = false
      sessionActive.value = false
      uploadedFiles.value = []
    } catch (error) {
      console.error('[Session] 退出演示模式失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // ==================== 文件管理 ====================

  /**
   * 上传文件
   * @param {File} file - 要上传的文件
   */
  async function uploadFile(file) {
    try {
      isLoading.value = true
      const formData = new FormData()
      formData.append('file', file)

      const result = await api.uploadFile(formData)
      await loadUploadedFiles()
      return result
    } catch (error) {
      console.error('上传文件失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 加载已上传文件列表
   */
  async function loadUploadedFiles() {
    try {
      const files = await api.getFiles()
      uploadedFiles.value = files || []
      return files
    } catch (error) {
      console.error('加载文件列表失败:', error)
      return []
    }
  }

  /**
   * 删除文件
   * @param {string} filename - 文件名
   */
  async function deleteFile(filename) {
    try {
      isLoading.value = true
      await api.deleteFile(filename)
      await loadUploadedFiles()
    } catch (error) {
      console.error('删除文件失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 清除所有数据
   */
  async function clearAllData() {
    try {
      isLoading.value = true
      await api.clearData()
      uploadedFiles.value = []
      if (isDemo.value) {
        await exitDemoMode()
      }
    } catch (error) {
      console.error('清除数据失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // ==================== 会话状态 ====================

  /**
   * 加载会话状态
   */
  async function loadSessionStatus() {
    try {
      console.log('[Session] Loading session status...')
      const status = await api.getSessionStatus()
      console.log('[Session] Session status:', status)

      // 更新会话活跃状态
      const wasActive = sessionActive.value
      sessionActive.value = status.active || false

      // 如果后端会话已失效（active: false），但本地显示在演示模式，清除本地状态
      if (!status.active && isDemo.value) {
        console.log('[Session] Backend session inactive, clearing local demo mode')
        isDemo.value = false
      }

      // 如果本地显示在演示模式，但后端会话是活跃的，需要验证一下
      // 通过尝试加载数据来验证演示模式是否真的有效
      if (isDemo.value && status.active) {
        console.log('[Session] Demo mode active and session valid')
      }

      console.log('[Session] Session active set to:', sessionActive.value, '(isDemo:', isDemo.value, ')')
      return status
    } catch (error) {
      console.error('[Session] 加载会话状态失败:', error)
      // 如果请求失败，可能是后端未启动，保持现有状态不变
      return null
    }
  }

  return {
    // 状态
    isDemo,
    sessionActive,
    uploadedFiles,
    isLoading,

    // 计算属性
    hasData,

    // 方法
    enterDemoMode,
    exitDemoMode,
    uploadFile,
    loadUploadedFiles,
    deleteFile,
    clearAllData,
    loadSessionStatus
  }
})
