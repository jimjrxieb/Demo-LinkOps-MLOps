// src/store/useUserStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref({
    id: null,
    name: 'Jimmie',
    email: null,
    role: 'Agent Overseer',
    avatar: null,
    preferences: {
      theme: 'dark',
      notifications: true,
      autoSave: true,
    },
    permissions: ['read', 'write', 'admin'],
  });

  const isAuthenticated = ref(false);
  const sessionToken = ref(null);
  const lastActivity = ref(null);

  // Getters
  const getUserName = computed(() => user.value.name);
  const getUserRole = computed(() => user.value.role);
  const getUserPreferences = computed(() => user.value.preferences);
  const hasPermission = computed(() => {
    return (permission) => user.value.permissions.includes(permission);
  });

  // Actions
  const login = (userData, token) => {
    user.value = { ...user.value, ...userData };
    sessionToken.value = token;
    isAuthenticated.value = true;
    lastActivity.value = new Date().toISOString();
  };

  const logout = () => {
    user.value = {
      id: null,
      name: 'Jimmie',
      email: null,
      role: 'Agent Overseer',
      avatar: null,
      preferences: {
        theme: 'dark',
        notifications: true,
        autoSave: true,
      },
      permissions: ['read', 'write', 'admin'],
    };
    sessionToken.value = null;
    isAuthenticated.value = false;
    lastActivity.value = null;
  };

  const updateUser = (updates) => {
    user.value = { ...user.value, ...updates };
  };

  const updatePreferences = (preferences) => {
    user.value.preferences = { ...user.value.preferences, ...preferences };
  };

  const updateActivity = () => {
    lastActivity.value = new Date().toISOString();
  };

  const setTheme = (theme) => {
    user.value.preferences.theme = theme;
  };

  return {
    // State
    user,
    isAuthenticated,
    sessionToken,
    lastActivity,

    // Getters
    getUserName,
    getUserRole,
    getUserPreferences,
    hasPermission,

    // Actions
    login,
    logout,
    updateUser,
    updatePreferences,
    updateActivity,
    setTheme,
  };
});
