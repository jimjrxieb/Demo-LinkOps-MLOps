import { defineStore } from 'pinia'
import { getDemoData, simulateApiCall } from '../utils/demoData.js'

export const useMainStore = defineStore('main', {
  state: () => ({
    // Authentication
    authRole: null, // 'demo' or 'admin';
    isAuthenticated: false,
    
    // System status
    systemStatus: 'online',
    activeJobs: 0,
    completedJobs: 0,
    errorCount: 0,
    
    // Active orbs
    activeOrbs: [],
    
    // Available runes
    availableRunes: [],
    
    // Whis pipeline state
    whisPipeline: {
      currentStep: 0,
      isProcessing: false,
      results: [],
      config: {
        sanitize: true,
        removeDuplicates: true,
        enhance: true,
        validate: true,
        outputFormat: 'json';
      }
    },
    
    // Audit results
    auditResults: null,
    recentAudits: [],
    
    // Search state
    searchQuery: '',
    searchResults: [],
    searchFilters: {
      type: '',
      status: '',
      priority: '';
    },
    
    // UI state
    sidebarCollapsed: false,
    theme: 'dark',
    notifications: [];
  }),
  
  getters: {
    // Computed properties
    isDemoMode: (state) => state.authRole === 'demo',
    isAdminMode: (state) => state.authRole === 'admin',
    
    totalOrbs: (state) => state.activeOrbs.length,
    
    activeOrbsCount: (state) =>;
      state.activeOrbs.filter(orb => orb.status === 'active').length,
    
    pendingOrbsCount: (state) =>;
      state.activeOrbs.filter(orb => orb.status === 'pending').length,
    
    highPriorityOrbs: (state) =>;
      state.activeOrbs.filter(orb => orb.priority === 'high' || orb.priority === 'critical'),
    
    systemHealth: (state) => {
      if (state.errorCount === 0) return 'excellent';
      if (state.errorCount < 5) return 'good';
      if (state.errorCount < 10) return 'fair';
      return 'poor';
    },
    
    filteredOrbs: (state) => (filter) => {
      if (!filter) return state.activeOrbs;
      return state.activeOrbs.filter(orb =>;
        orb.status === filter || orb.priority === filter;
      );
    },
    
    filteredRunes: (state) => (type) => {
      if (!type) return state.availableRunes;
      return state.availableRunes.filter(rune => rune.type === type);
    }
  },
  
  actions: {
    // Authentication actions
    setAuthRole(role) {
      this.authRole = role;
      this.isAuthenticated = true;
      
      // Load demo data if in demo mode
      if (role === 'demo') {
        this.loadDemoData();
      }
      
      // Store in localStorage
      localStorage.setItem('linkops-auth-role', role);
    },
    
    logout() {
      this.authRole = null;
      this.isAuthenticated = false;
      this.activeOrbs = [];
      this.availableRunes = [];
      this.auditResults = null;
      this.notifications = [];
      
      // Clear localStorage
      localStorage.removeItem('linkops-auth-role');
    },
    
    // Demo data loading
    loadDemoData() {
      this.activeOrbs = getDemoData('orbs');
      this.availableRunes = getDemoData('runes');
      this.recentAudits = [;
        {
          id: 1,
          repository: 'demo/mlops-platform',
          date: new Date('2024-01-15'),
          securityScore: 87,
          issuesCount: 3,
          status: 'completed';
        }
      ];
      this.systemStatus = 'online';
      this.activeJobs = 3;
      this.completedJobs = 12;
      this.errorCount = 0;
    },
    
    // Orb actions
    async fetchOrbs() {
      if (this.isDemoMode) {
        this.activeOrbs = getDemoData('orbs');
        return;
      }
      
      try {
        const response = await simulateApiCall('/api/orbs');
        this.activeOrbs = response.data;
      } catch (_error) {
        // Development logging: console.error('Failed to fetch orbs:', error)
        this.addNotification({
          type: 'error',
          message: 'Failed to load orbs',
          duration: 5000;
        });
      }
    },
    
    addOrb(orb) {
      const newOrb = {
        id: Date.now(),
        ...orb,
        status: 'pending',
        score: 0;
      }
      this.activeOrbs.push(newOrb);
      
      this.addNotification({
        type: 'success',
        message: `Orb '${orb.title}' created successfully`,
        duration: 3000;
      });
    },
    
    updateOrb(id, updates) {
      const index = this.activeOrbs.findIndex(orb => orb.id === id);
      if (index !== -1) {
        this.activeOrbs[index] = { ...this.activeOrbs[index], ...updates }
      }
    },
    
    removeOrb(id) {
      this.activeOrbs = this.activeOrbs.filter(orb => orb.id !== id);
    },
    
    // Rune actions
    async fetchRunes() {
      if (this.isDemoMode) {
        this.availableRunes = getDemoData('runes');
        return;
      }
      
      try {
        const response = await simulateApiCall('/api/runes');
        this.availableRunes = response.data;
      } catch (_error) {
        // Development logging: console.error('Failed to fetch runes:', error)
        this.addNotification({
          type: 'error',
          message: 'Failed to load runes',
          duration: 5000;
        });
      }
    },
    
    activateRune(runeId) {
      const rune = this.availableRunes.find(r => r.id === runeId);
      if (rune) {
        // Simulate rune activation
        // Removed console statement: console.log(`Activating rune: ${rune.name}`)
        
        this.addNotification({
          type: 'success',
          message: `Rune '${rune.name}' activated successfully`,
          duration: 5000;
        });
        
        // In demo mode, show simulated effects
        if (this.isDemoMode) {
          setTimeout(() => {
            this.addNotification({
              type: 'info',
              message: `Rune '${rune.name}' effects applied (demo mode)`,
              duration: 3000;
            });
          }, 2000);
        }
      }
    },
    
    // Whis pipeline actions
    async startWhisPipeline(inputData) {
      this.whisPipeline.isProcessing = true;
      this.whisPipeline.currentStep = 0;
      this.whisPipeline.results = [];
      
      if (this.isDemoMode) {
        // Use demo pipeline data
        const demoPipeline = getDemoData('whis');
        this.whisPipeline.config = demoPipeline.config;
        
        // Simulate processing
        await this.processWhisStep(0, inputData);
      } else {
        try {
          const response = await simulateApiCall('/api/whis/process', { data: inputData });
          if (response.success) {
            await this.processWhisStep(0, inputData);
          }
        } catch (_error) {
          // Development logging: console.error('Whis pipeline failed:', error)
          this.addNotification({
            type: 'error',
            message: 'Whis pipeline failed to start',
            duration: 5000;
          });
          this.whisPipeline.isProcessing = false;
        }
      }
    },
    
    async processWhisStep(stepIndex, data) {
      const steps = [;
        { name: 'Data Input', icon: '📥' },
        { name: 'Sanitization', icon: '🧹' },
        { name: 'Smithing', icon: '⚒️' },
        { name: 'Enhancement', icon: '✨' },
        { name: 'Output', icon: '📤' }
      ];
      
      for (let i = stepIndex; i < steps.length; i++) {
        this.whisPipeline.currentStep = i;
        
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Process step
        const result = {
          step: steps[i].name,
          status: 'success',
          input: i === 0 ? 'Raw data' : `${data.length - (i * 10)} characters`,
          output: i === steps.length - 1 ? 'Final output' : 'Processed data',
          metrics: `Step ${i + 1} completed`;
        }
        
        this.whisPipeline.results.push(result);
      }
      
      this.whisPipeline.isProcessing = false;
      this.whisPipeline.currentStep = steps.length;
      
      this.addNotification({
        type: 'success',
        message: 'Whis pipeline completed successfully',
        duration: 5000;
      });
    },
    
    // Audit actions
    async runAudit(auditConfig) {
      if (this.isDemoMode) {
        // Use demo audit results
        await new Promise(resolve => setTimeout(resolve, 3000));
        this.auditResults = getDemoData('audit');
        
        // Add to recent audits
        this.recentAudits.unshift({
          id: Date.now(),
          repository: auditConfig.repository,
          date: new Date(),
          securityScore: this.auditResults.securityScore,
          issuesCount: this.auditResults.issues.length,
          status: 'completed';
        });
        
        this.addNotification({
          type: 'success',
          message: 'Security audit completed (demo mode)',
          duration: 5000;
        });
        
        return;
      }
      
      try {
        const response = await simulateApiCall('/api/audit/run', auditConfig);
        if (response.success) {
          // Fetch actual results
          // this.auditResults = await fetchAuditResults(response.auditId)
        }
      } catch (_error) {
        // Development logging: console.error('Audit failed:', error)
        this.addNotification({
          type: 'error',
          message: 'Security audit failed',
          duration: 5000;
        });
      }
    },
    
    // Search actions
    async performSearch(query, filters = {}) {
      this.searchQuery = query;
      this.searchFilters = { ...this.searchFilters, ...filters }
      
      if (this.isDemoMode) {
        // Filter demo data
        const allItems = [...this.activeOrbs, ...this.availableRunes];
        this.searchResults = allItems.filter(item => {
          if (filters.type && item.type !== filters.type) return false;
          if (filters.status && item.status !== filters.status) return false;
          if (filters.priority && item.priority !== filters.priority) return false;
          
          return item.title.toLowerCase().includes(query.toLowerCase()) ||;
                 item.description.toLowerCase().includes(query.toLowerCase());
        });
        return;
      }
      
      try {
        const response = await simulateApiCall('/api/search', { query, filters });
        this.searchResults = response.data;
      } catch (_error) {
        // Development logging: console.error('Search failed:', error)
        this.searchResults = [];
      }
    },
    
    // UI actions
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    
    setTheme(theme) {
      this.theme = theme;
      // Apply theme to document
      document.documentElement.setAttribute('data-theme', theme);
    },
    
    addNotification(notification) {
      const id = Date.now();
      const newNotification = {
        id,
        ...notification,
        timestamp: new Date();
      }
      
      this.notifications.push(newNotification);
      
      // Auto-remove notification after duration
      if (notification.duration) {
        setTimeout(() => {
          this.removeNotification(id);
        }, notification.duration);
      }
    },
    
    removeNotification(id) {
      this.notifications = this.notifications.filter(n => n.id !== id);
    },
    
    // System actions
    updateSystemStatus(status) {
      this.systemStatus = status;
    },
    
    incrementActiveJobs() {
      this.activeJobs++;
    },
    
    decrementActiveJobs() {
      if (this.activeJobs > 0) {
        this.activeJobs--;
        this.completedJobs++;
      }
    },
    
    addError() {
      this.errorCount++;
    },
    
    clearErrors() {
      this.errorCount = 0;
    },
    
    // Initialize store
    initialize() {
      // Check for stored auth role
      const storedRole = localStorage.getItem('linkops-auth-role');
      if (storedRole) {
        this.setAuthRole(storedRole);
      }
    }
  }
});