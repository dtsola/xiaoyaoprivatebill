<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ background: `${iconColor}15` }">
      <i :class="icon" :style="{ color: iconColor }"></i>
    </div>
    <div class="stat-content">
      <p class="stat-title">{{ title }}</p>
      <p class="stat-value">{{ value }}</p>
      <div v-if="change !== null && change !== undefined" class="stat-change" :class="changeClass">
        <i :class="changeIcon"></i>
        <span>{{ changeText }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  change: {
    type: Number,
    default: null
  },
  icon: {
    type: String,
    default: 'fas fa-chart-line'
  },
  color: {
    type: String,
    default: '#007AFF'
  }
})

const iconColor = computed(() => props.color)

const changeClass = computed(() => {
  if (props.change === null || props.change === undefined) return ''
  return props.change > 0 ? 'positive' : props.change < 0 ? 'negative' : 'neutral'
})

const changeIcon = computed(() => {
  if (props.change === null || props.change === undefined) return 'fas fa-minus'
  return props.change > 0 ? 'fas fa-arrow-up' : props.change < 0 ? 'fas fa-arrow-down' : 'fas fa-minus'
})

const changeText = computed(() => {
  if (props.change === null || props.change === undefined) return ''
  const sign = props.change > 0 ? '+' : ''
  return `${sign}${props.change.toFixed(1)}%`
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.stat-icon i {
  font-size: 24px;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-title {
  font-size: 13px;
  color: var(--secondary-text);
  margin: 0 0 4px 0;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stat-change.positive {
  color: var(--success-color);
}

.stat-change.negative {
  color: var(--danger-color);
}

.stat-change.neutral {
  color: var(--secondary-text);
}
</style>
