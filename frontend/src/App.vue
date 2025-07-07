<template>
  <div id="app" class="animated-bg min-h-screen">
    <!-- Futuristic Navigation Bar -->
    <nav class="glass-panel fixed top-0 left-0 right-0 z-50 mx-4 mt-4 p-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center space-x-4">
          <div class="futuristic-title text-2xl text-white">
            LINKOPS-MLOPS
          </div>
          <div class="text-sm text-gray-300">
            Unified MLOps Platform
          </div>
        </div>

        <!-- Platform Navigation -->
        <div class="flex items-center space-x-2">
          <router-link 
            v-for="section in platformSections" 
            :key="section.name"
            :to="section.route"
            class="platform-nav-item glass-panel p-3 rounded-lg transition-all duration-300"
            :class="[
              `section-${section.name.toLowerCase()}`,
              { 'neon-border': $route.path === section.route }
            ]"
          >
            <div class="flex items-center space-x-2">
              <div 
                class="status-indicator"
                :class="section.status === 'online' ? 'status-online' : 
                       section.status === 'processing' ? 'status-processing' : 'status-offline'"
              ></div>
              <span class="futuristic-subtitle text-sm">{{ section.displayName }}</span>
            </div>
          </router-link>
          
          <!-- About Link -->
          <router-link 
            to="/about"
            class="platform-nav-item glass-panel p-3 rounded-lg transition-all duration-300"
            :class="{ 'neon-border': $route.path === '/about' }"
          >
            <div class="flex items-center space-x-2">
              <div class="status-indicator status-online"></div>
              <span class="futuristic-subtitle text-sm">About</span>
            </div>
          </router-link>
        </div>

        <!-- System Status -->
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-300">
            <span class="status-indicator status-online"></span>
            Platform Online
          </div>
          <div class="text-xs text-gray-400">
            {{ currentTime }}
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="pt-24 px-4 pb-8">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Platform Activity Stream Sidebar -->
    <div class="fixed right-4 top-24 bottom-4 w-80 glass-panel p-4 overflow-hidden">
      <h3 class="futuristic-subtitle text-lg mb-4">Platform Activity</h3>
      <div class="space-y-3 max-h-full overflow-y-auto">
        <div 
          v-for="activity in activityStream" 
          :key="activity.id"
          class="activity-item glass-panel p-3 rounded-lg"
          :class="`section-${activity.section.toLowerCase()}`"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium">{{ activity.section }}</span>
            <span class="text-xs text-gray-400">{{ activity.timestamp }}</span>
          </div>
          <p class="text-xs text-gray-300">{{ activity.description }}</p>
          <div class="activity-bar mt-2" :style="{ width: activity.intensity + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const currentTime = ref('')
    const activityStream = ref([
      {
        id: 1,
        section: 'Tasks',
        description: 'New MLOps task created',
        timestamp: '2m ago',
        intensity: 85
      },
      {
        id: 2,
        section: 'Scripts',
        description: 'Kubernetes deployment script executed',
        timestamp: '5m ago',
        intensity: 78
      },
      {
        id: 3,
        section: 'Orbs',
        description: 'New training orb generated',
        timestamp: '8m ago',
        intensity: 92
      },
      {
        id: 4,
        section: 'Runes',
        description: 'Model optimization rune activated',
        timestamp: '12m ago',
        intensity: 88
      }
    ])

    const platformSections = ref([
      { name: 'dashboard', displayName: 'Dashboard', route: '/dashboard', status: 'online' },
      { name: 'tasks', displayName: 'Tasks', route: '/tasks', status: 'online' },
      { name: 'scripts', displayName: 'Scripts', route: '/scripts', status: 'online' },
      { name: 'workflows', displayName: 'Workflows', route: '/workflows', status: 'online' },
      { name: 'orbs', displayName: 'Orbs', route: '/orbs', status: 'processing' },
      { name: 'runes', displayName: 'Runes', route: '/runes', status: 'online' },
      { name: 'digest', displayName: 'Digest', route: '/digest', status: 'online' }
    ])

    let timeInterval

    const updateTime = () => {
      const now = new Date()
      currentTime.value = now.toLocaleTimeString('en-US', { 
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    onMounted(() => {
      updateTime()
      timeInterval = setInterval(updateTime, 1000)
    })

    onUnmounted(() => {
      if (timeInterval) {
        clearInterval(timeInterval)
      }
    })

    return {
      currentTime,
      platformSections,
      activityStream
    }
  }
}
</script>

<style>
@import './assets/futuristic.css';

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Platform navigation hover effects */
.platform-nav-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.platform-nav-item.section-dashboard:hover {
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.platform-nav-item.section-tasks:hover {
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.platform-nav-item.section-scripts:hover {
  box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
}

.platform-nav-item.section-workflows:hover {
  box-shadow: 0 8px 25px rgba(168, 85, 247, 0.3);
}

.platform-nav-item.section-orbs:hover {
  box-shadow: 0 8px 25px rgba(236, 72, 153, 0.3);
}

.platform-nav-item.section-runes:hover {
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3);
}

.platform-nav-item.section-digest:hover {
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
}

/* Activity stream animations */
.activity-item {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Activity bar styling */
.activity-bar {
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 2px;
  transition: width 0.3s ease;
}
</style> 