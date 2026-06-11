<template>
  <div class="card">
    <h2>Skills ({{ skills.length }})</h2>
    <table v-if="skills.length">
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Description</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="skill in skills" :key="skill.id">
          <td><strong>{{ skill.name }}</strong></td>
          <td>
            <span class="badge badge-category">{{ skill.category }}</span>
          </td>
          <td>{{ skill.description || '-' }}</td>
          <td>
            <span :class="['badge', skill.enabled ? 'badge-enabled' : 'badge-disabled']">
              {{ skill.enabled ? 'Enabled' : 'Disabled' }}
            </span>
          </td>
          <td>
            <div class="actions">
              <button class="btn btn-primary" @click="$emit('toggle', skill)">
                {{ skill.enabled ? 'Disable' : 'Enable' }}
              </button>
              <button class="btn" @click="$emit('edit', skill)">Edit</button>
              <button class="btn btn-danger" @click="$emit('delete', skill.id)">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else style="text-align:center; color:#999; padding:20px;">
      No skills found. Add one above!
    </p>
  </div>
</template>

<script setup>
defineProps({
  skills: { type: Array, required: true }
})
defineEmits(['edit', 'delete', 'toggle'])
</script>

<style scoped>
.badge-category {
  background: #3498db;
  color: white;
}
</style>