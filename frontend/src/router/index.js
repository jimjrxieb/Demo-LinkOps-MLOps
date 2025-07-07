import { createRouter, createWebHistory } from 'vue-router'

// Import all views
import Dashboard from '@/views/Dashboard.vue'
import Tasks from '@/views/Tasks.vue'
import Scripts from '@/views/Scripts.vue'
import Workflows from '@/views/Workflows.vue'
import Orbs from '@/views/Orbs.vue'
import Runes from '@/views/Runes.vue'
import Digest from '@/views/Digest.vue'
import Login from '@/views/Login.vue'
import About from '@/views/About.vue'
import ArisePage from '@/views/ArisePage.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/arise', component: ArisePage },
  { path: '/dashboard', component: Dashboard },
  { path: '/tasks', component: Tasks },
  { path: '/scripts', component: Scripts },
  { path: '/workflows', component: Workflows },
  { path: '/orbs', component: Orbs },
  { path: '/runes', component: Runes },
  { path: '/digest', component: Digest },
  { path: '/login', component: Login },
  { path: '/about', component: About },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 