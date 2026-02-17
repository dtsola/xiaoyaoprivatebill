<template>
  <Teleport to="body">
    <div class="toast-container">
      <div
        class="toast"
        :class="[`toast-${uiStore.toast.type}`, { show: uiStore.toast.show }]"
      >
        <i :class="iconClass" class="toast-icon"></i>
        <span class="toast-message">{{ uiStore.toast.message }}</span>
        <button class="toast-close" @click="uiStore.hideToast">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useUiStore } from '@/stores/ui'
import { computed } from 'vue'

const uiStore = useUiStore()

const iconClass = computed(() => {
  const icons = {
    success: 'fas fa-check-circle',
    error: 'fas fa-exclamation-circle',
    warning: 'fas fa-exclamation-triangle',
    info: 'fas fa-info-circle'
  }
  return icons[uiStore.toast.type] || icons.info
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 300px;
  max-width: 500px;
  padding: 14px 16px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-float);
  pointer-events: auto;
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.3s ease;
}

.toast.show {
  opacity: 1;
  transform: translateY(0);
}

.toast-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.toast-success {
  border-left: 4px solid var(--success-color);
}

.toast-success .toast-icon {
  color: var(--success-color);
}

.toast-error {
  border-left: 4px solid var(--danger-color);
}

.toast-error .toast-icon {
  color: var(--danger-color);
}

.toast-warning {
  border-left: 4px solid var(--warning-color);
}

.toast-warning .toast-icon {
  color: var(--warning-color);
}

.toast-info {
  border-left: 4px solid var(--primary-color);
}

.toast-info .toast-icon {
  color: var(--primary-color);
}

.toast-message {
  flex: 1;
  font-size: 14px;
  color: var(--text-color);
}

.toast-close {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: var(--secondary-text);
  border-radius: var(--radius-sm);
}

.toast-close:hover {
  background: var(--hover-bg);
  color: var(--text-color);
}
</style>
