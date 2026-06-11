<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <h1>🎯 Skill Manager</h1>
        <div class="stats">
          <div class="stat">
            <span class="stat-value">{{ skills.length }}</span>
            <span class="stat-label">Total</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ enabledCount }}</span>
            <span class="stat-label">Enabled</span>
          </div>
        </div>
      </div>
    </header>

    <main class="main">
      <div class="toolbar">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search skills..."
            class="search-input"
          >
        </div>
        <button class="btn btn-primary" @click="showImportModal = true">
          📥 Import
        </button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else-if="filteredSkills.length === 0" class="empty">
        <div class="empty-icon">📭</div>
        <p v-if="searchQuery">No skills match "{{ searchQuery }}"</p>
        <p v-else>No skills found. Click Import to scan a directory.</p>
      </div>

      <div v-else class="card-grid">
        <SkillCard
          v-for="skill in filteredSkills"
          :key="skill.id"
          :skill="skill"
          @click="viewSkill(skill.id)"
          @toggle="toggleSkill"
        />
      </div>

      <!-- Import Modal -->
      <div v-if="showImportModal" class="modal-overlay" @click.self="showImportModal = false">
        <div class="modal">
          <h2>📥 Import Skills</h2>
          <div class="form-group">
            <label>Source Directory</label>
            <input v-model="importPath" type="text" placeholder="/Users/jiafei/.openclaw/openclaw/skills">
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="showImportModal = false">Cancel</button>
            <button class="btn btn-primary" @click="importSkills">Scan & Import</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import SkillCard from '../components/SkillCard.vue'

const router = useRouter()
const skills = ref([])
const searchQuery = ref('')
const loading = ref(true)
const showImportModal = ref(false)
const importPath = ref('')

const filteredSkills = computed(() => {
  if (!searchQuery.value) return skills.value
  const q = searchQuery.value.toLowerCase()
  return skills.value.filter(s =>
    s.name.toLowerCase().includes(q) ||
    (s.description && s.description.toLowerCase().includes(q))
  )
})

const enabledCount = computed(() => skills.value.filter(s => s.enabled).length)

const loadSkills = async () => {
  try {
    const res = await axios.get('/api/skills')
    skills.value = res.data
  } catch (err) {
    console.error('Failed to load skills:', err)
  } finally {
    loading.value = false
  }
}

const viewSkill = (id) => {
  router.push(`/skill/${id}`)
}

const toggleSkill = async (skill) => {
  try {
    await axios.put(`/api/skills/${skill.id}`, {
      enabled: !skill.enabled
    })
    skill.enabled = !skill.enabled
  } catch (err) {
    console.error('Failed to toggle skill:', err)
  }
}

const importSkills = async () => {
  if (!importPath.value) return
  try {
    await axios.post('/api/scan', { source_dir: importPath.value })
    showImportModal.value = false
    importPath.value = ''
    loadSkills()
  } catch (err) {
    alert('Import failed: ' + (err.response?.data?.error || err.message))
  }
}

onMounted(loadSkills)
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: var(--bg-primary);
}

.header {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card));
  padding: 24px 40px;
  border-bottom: 1px solid var(--border);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--accent-hover));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stats {
  display: flex;
  gap: 32px;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px;
}

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 15px;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
}

.loading, .empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 32px;
  width: 500px;
  max-width: 90vw;
  border: 1px solid var(--border);
}

.modal h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>