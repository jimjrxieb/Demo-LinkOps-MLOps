import { createRouter, createWebHistory } from 'vue-router'
import { useMainStore } from '@/store/useMainStore'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/DemoDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ml-builder',
    name: 'MLBuilder',
    component: () => import('@/views/MLBuilder.vue'),
    meta: { requiresAuth: true, requiresFull: true }
  },
  {
    path: '/pipeline',
    name: 'Pipeline',
    component: () => import('@/views/WhisPipeline.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/rag',
    name: 'RAG',
    component: () => import('@/views/RAGSearch.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const store = useMainStore()
  
  // Update activity timestamp and try silent refresh
  if (store.isAuthenticated) {
    store.updateActivity()
    await store.silentRefresh()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !store.isAuthenticated) {
    next('/login')
    return
  }

  // Check if route requires full access
  if (to.meta.requiresFull && !store.isFullAccess) {
    next('/')
    return
  }

  // If on login page and already authenticated, redirect to home
  if (to.path === '/login' && store.isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
