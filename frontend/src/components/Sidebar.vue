<template>
  <div class="sidebar" :class="{ 'sidebar-collapsed': collapsed }">
    <!-- Sidebar Header -->
    <div class="sidebar-header">
      <div class="logo-container">
        <div class="logo-icon">🛡️</div>
        <div v-if="!collapsed" class="logo-text">
          <h3>LinkOps</h3>
          <p>DevSecOps Demo</p>
        </div>
      </div>
      <button
        class="collapse-btn"
        :title="collapsed ? 'Expand' : 'Collapse'"
        @click="toggleCollapse"
      >
        <span v-if="!collapsed">◀</span>
        <span v-else>▶</span>
      </button>
    </div>

    <!-- Navigation Menu -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li v-for="item in menuItems" :key="item.path">
          <router-link
            :to="item.path"
            class="nav-item"
            :class="{ active: $route.path === item.path }"
            :title="collapsed ? item.title : ''"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span v-if="!collapsed" class="nav-text">{{ item.title }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Sidebar Footer -->
    <div class="sidebar-footer">
      <div class="demo-status">
        <span class="status-dot" />
        <span v-if="!collapsed" class="status-text">Demo Mode</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const collapsed = ref(false);

const menuItems = [
  {
    title: 'Demo Dashboard',
    path: '/',
    icon: '🧠',
  },
  {
    title: 'Task Processing',
    path: '/demo',
    icon: '🎯',
  },
  {
    title: 'Whis Pipeline',
    path: '/pipeline',
    icon: '⚙️',
  },
  {
    title: 'RAG Search',
    path: '/rag-search',
    icon: '🔍',
  },
  {
    title: 'Demo Sync',
    path: '/demo-sync',
    icon: '🔄',
  },
  {
    title: 'ML Builder',
    path: '/ml-builder',
    icon: '📊',
  },
  {
    title: 'Model Creator',
    path: '/model-creator',
    icon: '🤖',
  },
  {
    title: 'MCP Tool Creator',
    path: '/mcp-tool-creator',
    icon: '🔧',
  },
  {
    title: 'Tool Executor',
    path: '/execute-tool',
    icon: '⚡',
  },
  {
    title: 'Auto Runner',
    path: '/auto-runner',
    icon: '🚀',
  },
  {
    title: 'MCP Execution',
    path: '/mcp-execution',
    icon: '🛠️',
  },
  {
    title: 'Execution Logs',
    path: '/mcp-logs',
    icon: '🗒️',
  },
  {
    title: 'AI Chat',
    path: '/ai-chat',
    icon: '💬',
  },
  {
    title: 'HTC Feedback',
    path: '/htc',
    icon: '🧠',
  },
  {
    title: 'Reports',
    path: '/reports',
    icon: '📈',
  },
  {
    title: 'Orb Library',
    path: '/orbs',
    icon: '📚',
  },
  {
    title: 'Document Q&A',
    path: '/search-memory',
    icon: '📄',
  },
  {
    title: 'AI Feedback',
    path: '/htc-feedback',
    icon: '📝',
  },
  {
    title: 'AI Keywords',
    path: '/htc-prompt-editor',
    icon: '📓',
  },
  {
    title: 'Agent Builder',
    path: '/agent-builder',
    icon: '⚒️',
  },
  {
    title: 'Add API Keys',
    path: '/keys',
    icon: '🔑',
  },
  {
    title: 'About Demo',
    path: '/about',
    icon: 'ℹ️',
  },
];

const toggleCollapse = () => {
  collapsed.value = !collapsed.value;
};
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  border-right: 1px solid #334155;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.sidebar-collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid #334155;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 2rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 8px;
}

.logo-text h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
}

.logo-text p {
  margin: 0;
  font-size: 0.75rem;
  color: #94a3b8;
}

.collapse-btn {
  background: transparent;
  border: 1px solid #475569;
  color: #94a3b8;
  border-radius: 6px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.75rem;
}

.collapse-btn:hover {
  background: #475569;
  color: #f8fafc;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
  margin: 0.25rem 0;
}

.nav-item:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #f8fafc;
  border-left-color: #3b82f6;
}

.nav-item.active {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border-left-color: #3b82f6;
}

.nav-icon {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-weight: 500;
  white-space: nowrap;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #334155;
}

.demo-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 0.75rem;
  color: #22c55e;
  font-weight: 500;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }
}
</style>
