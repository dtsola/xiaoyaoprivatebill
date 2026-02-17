import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // 侧边栏状态
  const sidebarCollapsed = ref(false)

  // 加载状态
  const globalLoading = ref(false)

  // Toast 消息
  const toast = ref({
    show: false,
    message: '',
    type: 'info', // success, error, warning, info
    duration: 3000
  })

  // Modal 状态
  const modal = ref({
    show: false,
    title: '',
    component: null,
    props: {}
  })

  // ==================== 侧边栏 ====================

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setSidebarCollapsed(collapsed) {
    sidebarCollapsed.value = collapsed
  }

  // ==================== 加载状态 ====================

  function setGlobalLoading(loading) {
    globalLoading.value = loading
  }

  // ==================== Toast 消息 ====================

  function showToast(message, type = 'info', duration = 3000) {
    toast.value = {
      show: true,
      message,
      type,
      duration
    }

    if (duration > 0) {
      setTimeout(() => {
        hideToast()
      }, duration)
    }
  }

  function showSuccess(message, duration) {
    showToast(message, 'success', duration)
  }

  function showError(message, duration) {
    showToast(message, 'error', duration)
  }

  function showWarning(message, duration) {
    showToast(message, 'warning', duration)
  }

  function hideToast() {
    toast.value.show = false
  }

  // ==================== Modal ====================

  function showModal(title, component, props = {}) {
    modal.value = {
      show: true,
      title,
      component,
      props
    }
  }

  function hideModal() {
    modal.value.show = false
  }

  return {
    // 状态
    sidebarCollapsed,
    globalLoading,
    toast,
    modal,

    // 侧边栏方法
    toggleSidebar,
    setSidebarCollapsed,

    // 加载状态方法
    setGlobalLoading,

    // Toast 方法
    showToast,
    showSuccess,
    showError,
    showWarning,
    hideToast,

    // Modal 方法
    showModal,
    hideModal
  }
})
