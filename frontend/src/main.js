import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import axios from 'axios';

// Point axios at your API gateway.
// Default to localhost:9000 for development, can be overridden with VITE_API_URL
axios.defaults.baseURL =
  import.meta.env.VITE_API_URL || 'http://localhost:9000';

const pinia = createPinia();
createApp(App).use(pinia).use(router).mount('#app');
