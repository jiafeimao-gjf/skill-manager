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
      <span class="badge badge-category">{{ skill.category }}</span>
      <span class="file-count">📁 {{ skill.file_count || 0 }} files</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  skill: { type: Object, required: true }
})
defineEmits(['click', 'toggle'])
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

.file-count {
  color: var(--text-secondary);
  font-size: 13px;
}
</style>