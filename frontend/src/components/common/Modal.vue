<template>
  <Teleport to="body">
    <div class="modal-overlay" :class="{ show: uiStore.modal.show }" @click="handleOverlayClick">
      <div class="modal-container" :class="{ show: uiStore.modal.show }" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ uiStore.modal.title }}</h3>
          <button class="modal-close" @click="uiStore.hideModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <component v-if="uiStore.modal.component" :is="uiStore.modal.component" v-bind="uiStore.modal.props" />
          <div v-else>{{ uiStore.modal.props.content || '' }}</div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()

function handleOverlayClick() {
  uiStore.hideModal()
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.modal-overlay.show {
  opacity: 1;
  visibility: visible;
}

.modal-container {
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-float);
  transform: scale(0.9);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.modal-container.show {
  transform: scale(1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--secondary-text);
  border-radius: var(--radius-sm);
}

.modal-close:hover {
  background: var(--hover-bg);
  color: var(--text-color);
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}
</style>
