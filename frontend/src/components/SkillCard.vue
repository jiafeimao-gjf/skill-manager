<template>
  <div class="card" @click="$emit('click')">
    <div class="card-header">
      <h3 class="card-title">{{ skill.name }}</h3>
      <span :class="['badge', skill.enabled ? 'badge-enabled' : 'badge-disabled']">
        {{ skill.enabled ? 'Enabled' : 'Disabled' }}
      </span>
    </div>
    <p class="card-desc">{{ skill.description || 'No description' }}</p>
    <div class="card-footer">
      <span :class="['badge', 'badge-category', 'cat-' + funcCategory]">
        {{ funcIcon }} {{ funcCategory }}
      </span>
      <span class="file-count">📁 {{ skill.file_count || 0 }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  skill: { type: Object, required: true }
})
defineEmits(['click', 'toggle'])

const funcCategory = computed(() => props.skill.func_category || 'other')

const funcIcon = computed(() => {
  const icons = {
    code: '💻',
    writing: '✍️',
    research: '🔍',
    image: '🖼️',
    video: '🎬',
    audio: '🔊',
    ppt: '📊',
    excel: '📊',
    automation: '⚡',
    devops: '🚀',
    design: '🎨',
    data: '💾',
    communication: '💬',
    learning: '📚',
    other: '📦'
  }
  return icons[funcCategory.value] || '📁'
})
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: 0 8px 24px rgba(108, 92, 231, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 42px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-enabled {
  background: rgba(0, 184, 148, 0.2);
  color: var(--success);
}

.badge-disabled {
  background: rgba(255, 107, 107, 0.2);
  color: var(--danger);
}

.badge-category {
  background: rgba(108, 92, 231, 0.2);
  color: var(--accent-hover);
}

.cat-code { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.cat-writing { background: rgba(168, 85, 247, 0.2); color: #c084fc; }
.cat-research { background: rgba(236, 72, 153, 0.2); color: #f472b6; }
.cat-image { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
.cat-video { background: rgba(250, 204, 21, 0.2); color: #facc15; }
.cat-audio { background: rgba(251, 146, 60, 0.2); color: #fb923c; }
.cat-ppt { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
.cat-excel { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.cat-automation { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.cat-devops { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.cat-design { background: rgba(219, 112, 219, 0.2); color: #e879f9; }
.cat-data { background: rgba(6, 182, 212, 0.2); color: #22d3ee; }
.cat-communication { background: rgba(20, 184, 166, 0.2); color: #2dd4bf; }
.cat-learning { background: rgba(132, 204, 22, 0.2); color: #a3e635; }

.file-count {
  color: var(--text-secondary);
  font-size: 13px;
}
</style>