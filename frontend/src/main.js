import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useMainStore } from './store/useMainStore'

// Create app instance
const app = createApp(App)

// Setup Pinia store
const pinia = createPinia()
app.use(pinia)

// Setup router
app.use(router)

// Initialize the app
app.mount('#app')

// Initialize auth state
const store = useMainStore()
store.initializeAuth()
