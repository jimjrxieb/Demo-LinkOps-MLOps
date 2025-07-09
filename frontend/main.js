import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'

// Import views
import Dashboard from './views/Dashboard.vue'
import Whis from './views/Whis.vue'
import Audit from './views/Audit.vue'
import Login from './views/Login.vue'
import NotFound from './views/NotFound.vue'

// Import global styles
import './assets/holo-theme.css'
import './index.css'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [;
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard;
    },
    {
      path: '/whis',
      name: 'Whis',
      component: Whis;
    },
    {
      path: '/audit',
      name: 'Audit',
      component: Audit;
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound;
    }
  ];
});

// Create Pinia store
const pinia = createPinia();

// Create and mount app
const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount('#app');