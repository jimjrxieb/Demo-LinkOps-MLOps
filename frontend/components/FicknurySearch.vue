<template>;
  <div class="search-container">;
    <div class="search-box">;
      <div class="search-icon">🔍</div>;
      <input;
        v-model="searchQuery";
        type="text";
        placeholder="Search orbs, tasks, or repositories...";
        class="search-input";
        @input="handleSearch";
        @keyup.enter="performSearch";
      />;
      <button class="search-btn" @click="performSearch">;
        <span class="btn-icon">⚡</span>;
        Search;
      </button>;
    </div>;
    
    <!-- Search Filters -->;
    <div class="search-filters">;
      <div class="filter-group">;
        <label class="filter-label">Type:</label>;
        <select v-model="filters.type" class="filter-select">;
          <option value="">All Types</option>;
          <option value="orb">Orbs</option>;
          <option value="task">Tasks</option>;
          <option value="repository">Repositories</option>;
        </select>;
      </div>;
      
      <div class="filter-group">;
        <label class="filter-label">Status:</label>;
        <select v-model="filters.status" class="filter-select">;
          <option value="">All Status</option>;
          <option value="active">Active</option>;
          <option value="pending">Pending</option>;
          <option value="completed">Completed</option>;
        </select>;
      </div>;
      
      <div class="filter-group">;
        <label class="filter-label">Priority:</label>;
        <select v-model="filters.priority" class="filter-select">;
          <option value="">All Priorities</option>;
          <option value="critical">Critical</option>;
          <option value="high">High</option>;
          <option value="medium">Medium</option>;
          <option value="low">Low</option>;
        </select>;
      </div>;
    </div>;
    
    <!-- Search Results -->;
    <div v-if="searchResults.length > 0" class="search-results">;
      <h3 class="results-title">Search Results ({{ searchResults.length }})</h3>;
      <div class="results-list">;
        <div;
          v-for="result in searchResults";
          :key="result.id";
          class="result-item";
          @click="selectResult(result)";
        >;
          <div class="result-icon">{{ result.icon }}</div>;
          <div class="result-content">;
            <h4 class="result-title">{{ result.title }}</h4>;
            <p class="result-description">{{ result.description }}</p>;
            <div class="result-meta">;
              <span class="result-type">{{ result.type }}</span>;
              <span class="result-status" :class="result.status">{{ result.status }}</span>;
            </div>;
          </div>;
        </div>;
      </div>;
    </div>;
    
    <!-- No Results -->;
    <div v-else-if="hasSearched && searchQuery" class="no-results">;
      <div class="no-results-icon">🔍</div>;
      <h3>No results found</h3>;
      <p>Try adjusting your search terms or filters</p>;
    </div>;
  </div>;
</template>;

<script>;
export default {
  name: 'FicknurySearch',
  data() {
    return {
      searchQuery: '',
      hasSearched: false,
      filters: {
        type: '',
        status: '',
        priority: '';
      },
      searchResults: [],
      debounceTimer: null;
    }
  },
  methods: {
    handleSearch() {
      // Debounce search to avoid too many API calls
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.performSearch();
      }, 300);
    },
    
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        this.hasSearched = false;
        return;
      }
      
      this.hasSearched = true;
      
      try {
        // Simulate API call - replace with actual API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Mock search results
        this.searchResults = [;
          {
            id: 1,
            type: 'orb',
            title: 'Data Pipeline Optimization',
            description: 'Optimize ML data processing pipeline for faster training',
            status: 'active',
            icon: '🔮',
            priority: 'high';
          },
          {
            id: 2,
            type: 'task',
            title: 'Security Audit - Frontend',
            description: 'Run comprehensive security scan on frontend codebase',
            status: 'pending',
            icon: '📋',
            priority: 'critical';
          },
          {
            id: 3,
            type: 'repository',
            title: 'linkops/mlops-platform',
            description: 'Main MLOps platform repository',
            status: 'active',
            icon: '📁',
            priority: 'high';
          }
        ].filter(result => {
          // Apply filters
          if (this.filters.type && result.type !== this.filters.type) return false;
          if (this.filters.status && result.status !== this.filters.status) return false;
          if (this.filters.priority && result.priority !== this.filters.priority) return false;
          
          // Apply search query
          const query = this.searchQuery.toLowerCase();
          return result.title.toLowerCase().includes(query) ||;
                 result.description.toLowerCase().includes(query);
        });
        
        this.$emit('search', {
          query: this.searchQuery,
          filters: this.filters,
          results: this.searchResults;
        });
        
      } catch (_error) {
        // Development logging: console.error('Search failed:', error)
        this.searchResults = [];
      }
    },
    
    selectResult(result) {
      this.$emit('select-result', result);
    }
  }
}
</script>;

<style scoped>;
.search-container {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-icon {
  font-size: 1.5rem;
  color: #00d4ff;
}

.search-input {
  flex: 1;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #e0e0e0;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.search-input::placeholder {
  color: #666;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.1rem;
}

.search-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  font-weight: bold;
}

.filter-select {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 6px;
  padding: 0.5rem;
  color: #e0e0e0;
  font-size: 0.9rem;
  min-width: 120px;
}

.filter-select:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.search-results {
  margin-top: 1.5rem;
}

.results-title {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.result-item:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  transform: translateX(5px);
}

.result-icon {
  font-size: 1.5rem;
  min-width: 40px;
  text-align: center;
}

.result-content {
  flex: 1;
}

.result-title {
  color: #00d4ff;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.result-description {
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.result-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.result-type {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: bold;
}

.result-status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.result-status.active {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.result-status.pending {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.result-status.completed {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #888;
}

.no-results-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-results h3 {
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .search-box {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .search-input {
    width: 100%;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .filter-select {
    min-width: auto;
  }
  
  .result-item {
    flex-direction: column;
    text-align: center;
  }
  
  .result-meta {
    justify-content: center;
  }
}
</style>;