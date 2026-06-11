import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SkillDetail from '../views/SkillDetail.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/skill/:id', name: 'SkillDetail', component: SkillDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router