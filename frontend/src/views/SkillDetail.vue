<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <button class="back-btn" @click="goBack">← Back</button>
        <div class="skill-info" v-if="skill">
          <h1>{{ skill.name }}</h1>
          <p class="skill-desc">{{ skill.description }}</p>
        </div>
      </div>
    </header>

    <main class="main">
      <div v-if="loading" class="loading">Loading...</div>

      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else class="content-layout">
        <aside class="file-list">
          <h3>📁 Files ({{ files.length }})</h3>
          <div
            v-for="file in files"
            :key="file.id"
            :class="['file-item', { active: selectedFile?.id === file.id }]"
            @click="selectFile(file)"
          >
            <span class="file-icon">{{ getFileIcon(file.file_type) }}</span>
            <span class="file-name">{{ file.filename }}</span>
          </div>
        </aside>

        <div class="file-preview">
          <div v-if="!selectedFile" class="preview-placeholder">
            <span>📄</span>
            <p>Select a file to preview</p>
          </div>
          <div v-else-if="selectedFile.file_type === 'markdown'" class="markdown-content" v-html="renderedContent"></div>
          <pre v-else class="raw-content">{{ fileContent }}</pre>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'

const router = useRouter()
const route = useRoute()

const skill = ref(null)
const files = ref([])
const selectedFile = ref(null)
const fileContent = ref('')
const loading = ref(true)
const error = ref('')

const renderedContent = ref('')

const goBack = () => router.push('/')

const loadSkill = async () => {
  try {
    const res = await axios.get(`/api/skills/${route.params.id}`)
    skill.value = res.data.skill
    files.value = res.data.files
  } catch (err) {
    error.value = 'Failed to load skill'
  } finally {
    loading.value = false
  }
}

const selectFile = async (file) => {
  selectedFile.value = file
  try {
    const res = await axios.get(`/api/files/${file.id}`, { responseType: 'text' })
    fileContent.value = res.data
    if (file.file_type === 'markdown') {
      renderedContent.value = marked(fileContent.value)
    }
  } catch (err) {
    fileContent.value = 'Failed to load file content'
  }
}

const getFileIcon = (type) => {
  const icons = {
    markdown: '📝',
    json: '📋',
    python: '🐍',
    javascript: '📜',
    shell: '⚙️',
    yaml: '📐',
    text: '📄'
  }
  return icons[type] || '📄'
}

onMounted(loadSkill)
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: var(--bg-primary);
}

.header {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card));
  padding: 20px 40px;
  border-bottom: 1px solid var(--border);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 24px;
}

.back-btn {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  color: var(--text-primary);
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.back-btn:hover {
  background: var(--border);
}

.skill-info h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.skill-desc {
  color: var(--text-secondary);
  margin-top: 4px;
}

.main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px;
}

.loading, .error, .preview-placeholder {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.content-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
  height: calc(100vh - 200px);
}

.file-list {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border);
  overflow-y: auto;
}

.file-list h3 {
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.file-item:hover {
  background: var(--bg-secondary);
}

.file-item.active {
  background: var(--accent);
  color: white;
}

.file-icon {
  font-size: 18px;
}

.file-name {
  font-size: 14px;
  word-break: break-all;
}

.file-preview {
  background: var(--bg-card);
  border-radius: 12px;
  border: 1px solid var(--border);
  overflow: hidden;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 48px;
}

.preview-placeholder p {
  margin-top: 16px;
}

.markdown-content, .raw-content {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.6;
}

.markdown-content {
  color: var(--text-primary);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  color: var(--accent);
  margin: 16px 0 8px;
}

.markdown-content :deep(code) {
  background: var(--bg-secondary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.markdown-content :deep(pre) {
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.raw-content {
  background: var(--bg-secondary);
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-all;
}

@media (max-width: 768px) {
  .content-layout {
    grid-template-columns: 1fr;
    height: auto;
  }

  .file-list {
    max-height: 200px;
  }
}
</style>