import { createRouter, createWebHistory } from 'vue-router'

// Import views
import Demo from '../views/Demo.vue'
import WhisPipeline from '../views/WhisPipeline.vue'
import OrbLibrary from '../views/OrbLibrary.vue'
import AddKeys from '../views/AddKeys.vue'
import AboutDemo from '../views/AboutDemo.vue'

// Import new demo views
import MLCreator from '../views/MLCreator.vue'
import AgentCreator from '../views/AgentCreator.vue'
import HTC from '../views/HTC.vue'
import Reports from '../views/Reports.vue'

// Import demo components
import DemoRAG from '../components/DemoRAG.vue'
import DemoPipeline from '../components/DemoPipeline.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Demo
  },
  {
    path: '/pipeline',
    name: 'WhisPipeline',
    component: WhisPipeline
  },
  {
    path: '/orbs',
    name: 'OrbLibrary',
    component: OrbLibrary
  },
  {
    path: '/keys',
    name: 'AddKeys',
    component: AddKeys
  },
  {
    path: '/about',
    name: 'AboutDemo',
    component: AboutDemo
  },
  // New demo routes with unified API
  {
    path: '/ml',
    name: 'MLCreator',
    component: MLCreator
  },
  {
    path: '/agents',
    name: 'AgentCreator',
    component: AgentCreator
  },
  {
    path: '/htc',
    name: 'HTC',
    component: HTC
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  },
  // Legacy demo routes (for backward compatibility)
  {
    path: '/demo/rag',
    name: 'DemoRAG',
    component: DemoRAG
  },
  {
    path: '/demo/pipeline',
    name: 'DemoPipeline',
    component: DemoPipeline
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 