import { createRouter, createWebHistory } from 'vue-router'
import { useMainStore } from '../store/index.js'

// Import views
import Dashboard from '../views/Dashboard.vue'
import Whis from '../views/Whis.vue'
import Audit from '../views/Audit.vue'
import Login from '../views/Login.vue'
import NotFound from '../views/NotFound.vue'

const routes = [;
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login - LinkOps MLOps',
      requiresAuth: false;
    }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: 'Dashboard - LinkOps MLOps',
      requiresAuth: true;
    }
  },
  {
    path: '/whis',
    name: 'Whis',
    component: Whis,
    meta: {
      title: 'Whis Pipeline - LinkOps MLOps',
      requiresAuth: true;
    }
  },
  {
    path: '/audit',
    name: 'Audit',
    component: Audit,
    meta: {
      title: 'Security Audit - LinkOps MLOps',
      requiresAuth: true;
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: 'Page Not Found - LinkOps MLOps',
      requiresAuth: false;
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes;
});

// Update page title on route change and handle authentication
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  
  // Check authentication
  const store = useMainStore();
  const requiresAuth = to.meta.requiresAuth;
  
  if (requiresAuth && !store.isAuthenticated) {
    // Redirect to login if not authenticated
    next('/login');
  } else if (to.path === '/login' && store.isAuthenticated) {
    // Redirect to dashboard if already authenticated
    next('/');
  } else {
    next();
  }
});

export default router 