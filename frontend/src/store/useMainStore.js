import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    user: 'Jimmie',
    agentMode: true,
    darkMode: true,
    isAuthenticated: false,
    currentView: 'dashboard',
    notifications: [],
    systemStatus: 'operational'
  }),
  
  getters: {
    getUserName: (state) => state.user,
    isAgentModeActive: (state) => state.agentMode,
    isDarkMode: (state) => state.darkMode,
    getSystemStatus: (state) => state.systemStatus,
    getCurrentView: (state) => state.currentView
  },
  
  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
    },
    
    toggleAgentMode() {
      this.agentMode = !this.agentMode
    },
    
    setUser(userName) {
      this.user = userName
    },
    
    setAuthenticationStatus(status) {
      this.isAuthenticated = status
    },
    
    setCurrentView(view) {
      this.currentView = view
    },
    
    addNotification(message, type = 'info') {
      this.notifications.push({
        id: Date.now(),
        message,
        type,
        timestamp: new Date().toISOString()
      })
    },
    
    removeNotification(id) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index > -1) {
        this.notifications.splice(index, 1)
      }
    },
    
    clearNotifications() {
      this.notifications = []
    },
    
    setSystemStatus(status) {
      this.systemStatus = status
    }
  }
}) 