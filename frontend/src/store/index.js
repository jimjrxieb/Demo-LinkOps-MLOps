// src/store/index.js
import { createPinia } from 'pinia';

const pinia = createPinia();
export default pinia;

// Export all stores for convenience
export { useMainStore } from './useMainStore';
export { useAgentStore } from './useAgentStore';
export { useTaskStore } from './useTaskStore';
export { useUserStore } from './useUserStore';
